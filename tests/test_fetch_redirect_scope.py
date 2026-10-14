from io import BytesIO
from pathlib import Path
from types import TracebackType
from typing import Any, Self
from config import sites
from main import main
import json
from uuid import UUID
import requests
import pytest
import i_work_for_sa


requested_urls: list[str] = []

class FakeSession:
    def __init__(self) -> None:
        self.headers: dict[str, Any] = {}

    def __enter__(self) -> Self:
        return self

    def __exit__(
        self,
        exc_type: type[BaseException] | None,
        exc: BaseException | None,
        tb: TracebackType | None,
    ) -> None:
        pass
    
    def get(self, url: str, **kwargs: Any) -> requests.Response:
        requested_urls.append(url)
        response = requests.Response()
        response.status_code = 302
        response.headers["Location"] = "https://evil.example.com/jb/page/test"
        response.raw = BytesIO(initial_bytes=b"")
        return response

class FakeClock:
    def __init__(self) -> None:
        self.current_time: float =0.0

    def monotonic(self)-> float:
        return self.current_time

    def sleep(self, seconds:float)-> None:
        self.current_time += seconds

class FakeSession2:
    def __init__(self,
                clock: FakeClock, 
                results_html: bytes = b"<html><body>Test results</body></html>",
                ) -> None:
        self.headers: dict[str, Any] = {}
        self.requests_made: list[str] = []
        self.request_log: list[tuple[str, str]] = []
        self.request_options: list[dict[str, Any]] = []
        self.clock: FakeClock = clock
        self.request_times: list[float] = []
        self.results_html: bytes = results_html

    def __enter__(self) -> Self:
        return self

    def __exit__(
        self,
        exc_type: type[BaseException] | None,
        exc: BaseException | None,
        tb: TracebackType | None,
    ) -> None:
        pass

    def get(self, url: str, **kwargs: Any) -> requests.Response:
        self.request_times.append(self.clock.monotonic())
        self.requests_made.append(url)
        self.request_log.append(("GET", url))
        self.request_options.append(kwargs.copy())
        response = requests.Response()
        if len(self.requests_made) == 1:
            response.status_code = 302
            response.headers["Location"] = "/jb/page/test-search"
            response.raw = BytesIO(initial_bytes=b" ")
        elif len(self.requests_made) == 2:
            response.status_code = 200
            html_string = b'<html><input name="jobboard_token" value="TEST_TOKEN"></html>'
            response.headers["Content-Type"] = "text/html"
            response.raw = BytesIO(initial_bytes=html_string)
        elif len(self.requests_made) == 3:
            response.status_code = 200
            response.headers["Content-Type"] = "text/html"
            response.raw = BytesIO(initial_bytes=self.results_html)
        return response

    def post(self, url: str, **kwargs: Any)-> requests.Response:
        self.request_times.append(self.clock.monotonic())
        self.request_log.append(("POST", url))
        self.request_options.append(kwargs.copy())
        response = requests.Response()
        response.status_code = 302
        response.headers["Location"] = "/jb/page/test-results"
        response.raw = BytesIO(initial_bytes=b" ")
        return response


class DotSegmentFakeSession(FakeSession):
    def get(self, url: str, **kwargs: Any) -> requests.Response:
        requested_urls.append(url)
        response = requests.Response()
        response.status_code = 302
        response.headers["Location"] = (
            "https://www.iworkfor.sa.gov.au/jb/page/../../not-approved/test")
        response.raw = BytesIO(initial_bytes=b"")
        return response

class EncodedDotSegmentFakeSession(FakeSession):
    def get(self, url: str, **kwargs: Any) -> requests.Response:
        requested_urls.append(url)
        response = requests.Response()
        response.status_code = 302
        response.headers["Location"] = (
            "/jb/page/%2e%2e/%2e%2e/not-approved/test")
        response.raw = BytesIO(initial_bytes=b"")
        return response

class AbsoluteEncodedDotSegmentFakeSession(FakeSession):
    def get(self, url: str, **kwargs: Any) -> requests.Response:
        requested_urls.append(url)
        response = requests.Response()
        response.status_code = 302
        response.headers["Location"] = (
            "https://www.iworkfor.sa.gov.au/jb/page/%2e%2e/%2e%2e/not-approved/test"
            )
        response.raw = BytesIO(initial_bytes=b"")
        return response

def test_end_to_end_uuid7(monkeypatch: pytest.MonkeyPatch, tmp_path: Path)-> None:
    fixture_path: Path = Path(__file__).parent / "fixtures" / "i_work_for_sa.html"
    fixture_html: bytes = fixture_path.read_bytes()
    fake_clock = FakeClock()
    fake_session = FakeSession2(clock=fake_clock, results_html=fixture_html)
    monkeypatch.setattr(
                        target=i_work_for_sa,
                        name="time", 
                        value=fake_clock
                        )
    monkeypatch.setattr(
                        target=i_work_for_sa.requests,
                        name="Session",
                        value=lambda: fake_session
                        )
    monkeypatch.chdir(path=tmp_path)

    main()
    search_path = tmp_path/"data"/"i_work_for_sa"
    file = list(search_path.glob("*.json"))

    assert len(file) == 1

    output_path = file[0]
    output_data = json.loads(output_path.read_text(encoding="utf-8"))
    run_id = output_data["metadata"]["run_id"]
    identifier = UUID(run_id)

    assert identifier.version == 7

def test_verify_http_request_boundary(monkeypatch: pytest.MonkeyPatch):
    requested_urls.clear()

    monkeypatch.setattr(
        target=i_work_for_sa.requests,
        name="Session",
        value=EncodedDotSegmentFakeSession
    )

    with pytest.raises(expected_exception=ValueError, match="Path Segment"):
        i_work_for_sa.fetch_job_listings_html()

    assert len(requested_urls) == 1
    assert requested_urls == [i_work_for_sa.sites["i_work_for_sa"]["job_search_url"]]

def test_verify_absolute_http_request_boundary(monkeypatch: pytest.MonkeyPatch):
    requested_urls.clear()

    monkeypatch.setattr(
        target=i_work_for_sa.requests,
        name="Session",
        value=AbsoluteEncodedDotSegmentFakeSession
    )

    with pytest.raises(expected_exception=ValueError, match="Path Segment"):
        i_work_for_sa.fetch_job_listings_html()

    assert len(requested_urls) == 1
    assert requested_urls == [sites["i_work_for_sa"]["job_search_url"]]

def test_sucessful_four_request_workflow(monkeypatch: pytest.MonkeyPatch) -> None:
    fake_clock = FakeClock()
    fake_session = FakeSession2(fake_clock)
    monkeypatch.setattr(target=i_work_for_sa.requests, name="Session", value=lambda: fake_session)
    monkeypatch.setattr(target=i_work_for_sa, name="time", value=fake_clock)
    result = i_work_for_sa.fetch_job_listings_html()
    methods = [record[0] for record in fake_session.request_log]
    post_data = fake_session.request_options[2]["data"]
    url_list = [record[1] for record in fake_session.request_log]

    assert result == b"<html><body>Test results</body></html>"
    assert methods == ["GET", "GET", "POST", "GET"]
    for options in fake_session.request_options:
        assert options["timeout"] == i_work_for_sa.REQUEST_TIMEOUT
        assert options["allow_redirects"] is False
    assert post_data["jobboard_token"] == "TEST_TOKEN"
    assert post_data["action"] == "Search"
    assert post_data["c_179[]"] == sites["i_work_for_sa"]["category_id"]
    assert url_list[0] == sites["i_work_for_sa"]["job_search_url"]
    assert url_list[1] == f"{sites['i_work_for_sa']['base_url']}/jb/page/test-search"
    assert url_list[2] == sites["i_work_for_sa"]["job_search_url"]
    assert url_list[3] == f"{sites['i_work_for_sa']['base_url']}/jb/page/test-results"
    for index in range(1, len(fake_session.request_times)):
        elapsed_time = fake_session.request_times[index] - fake_session.request_times[index - 1]
        assert elapsed_time >= i_work_for_sa.MIN_REQUEST_INTERVAL

def test_off_scope_redirect_is_not_fetched(monkeypatch: pytest.MonkeyPatch) -> None:
    requested_urls.clear()
    monkeypatch.setattr(target=i_work_for_sa.requests, name="Session", value=FakeSession)

    with pytest.raises(expected_exception=ValueError):
        i_work_for_sa.fetch_job_listings_html()

    assert len(requested_urls) == 1
    assert requested_urls[0] == i_work_for_sa.sites["i_work_for_sa"]["job_search_url"]

def test_dot_segment_redirect_is_not_fetched(monkeypatch: pytest.MonkeyPatch) -> None:
    requested_urls.clear()

    monkeypatch.setattr(
        target=i_work_for_sa.requests,
        name="Session",
        value=DotSegmentFakeSession
    )

    with pytest.raises(expected_exception=ValueError):
        i_work_for_sa.fetch_job_listings_html()

    assert len(requested_urls) == 1
    assert requested_urls[0] == i_work_for_sa.sites["i_work_for_sa"]["job_search_url"]

def test_malicious_redirect_form_root_relative():
    response = requests.Response()
    response.status_code = 302
    response.headers["Location"] = "/jb/page/%2e%2e/%2e%2e/not-approved/test" 
    response.raw = BytesIO(initial_bytes=b"")

    with pytest.raises(expected_exception=ValueError, match="Path Segment"):
        i_work_for_sa.validate_url_redirect(response)

def test_malicious_redirect_form_absolute():
    response = requests.Response()
    response.status_code = 302
    response.headers["Location"] = "https://www.iworkfor.sa.gov.au/jb/page/%2e%2e/%2e%2e/not-approved/test"
    response.raw = BytesIO(initial_bytes=b" ")

    with pytest.raises(expected_exception=ValueError, match="Path Segment"):
        i_work_for_sa.validate_url_redirect(response)