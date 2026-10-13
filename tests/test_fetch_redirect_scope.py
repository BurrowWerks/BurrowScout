from io import BytesIO
from types import TracebackType
from typing import Any, Self

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

class DotSegmentFakeSession(FakeSession):
    def get(self, url: str, **kwargs: Any) -> requests.Response:
        requested_urls.append(url)

        response = requests.Response()
        response.status_code = 302
        response.headers["Location"] = (
            "https://www.iworkfor.sa.gov.au/jb/page/../../not-approved/test"
        )
        response.raw = BytesIO(initial_bytes=b"")
        return response

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