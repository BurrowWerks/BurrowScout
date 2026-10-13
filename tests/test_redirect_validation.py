import requests
import pytest
from io import BytesIO
from i_work_for_sa import validate_url_redirect
from config import MAX_RESPONSE_SIZE

def test_validate_url_redirect_is_accepted() -> None:
    response = requests.Response()
    response.status_code = 302
    response.headers["Location"] = "/jb/page/test"
    response.raw = BytesIO()
    
    result: str = validate_url_redirect(response)
    
    assert result == "https://www.iworkfor.sa.gov.au/jb/page/test"


def test_validate_url_redirect_wrong_hostname() -> None:
    response = requests.Response()
    response.status_code = 302
    response.headers["Location"] = "https://evil.example.com/jb/page/test"
    response.raw = BytesIO()
    
    with pytest.raises(expected_exception=ValueError):    
        validate_url_redirect(response)


def test_validate_url_redirect_is_rejected_wrong_scheme() -> None:
    response = requests.Response()
    response.status_code = 302
    response.headers["Location"] = "http://www.iworkfor.sa.gov.au/jb/page/test"
    response.raw = BytesIO()
    
    with pytest.raises(expected_exception=ValueError):    
        validate_url_redirect(response)


def test_validate_url_redirect_is_rejected_wrong_path() -> None:
    response = requests.Response()
    response.status_code = 302
    response.headers["Location"] = "https://www.iworkfor.sa.gov.au/not-approved/test"
    response.raw = BytesIO()
    
    with pytest.raises(expected_exception=ValueError):    
        validate_url_redirect(response)


def test_validate_url_redirect_is_rejected_missing_location() -> None:
    response = requests.Response()
    response.status_code = 302
    response.raw = BytesIO()
    
    with pytest.raises(expected_exception=ValueError):    
        validate_url_redirect(response)


def test_validate_url_redirect_is_rejected_wrong_status_code() -> None:
    response = requests.Response()
    response.status_code = 200
    response.headers["Location"] = "/jb/page/test"
    
    with pytest.raises(expected_exception=ValueError):    
        validate_url_redirect(response)

def test_dot_segment_path_escape_is_rejected() -> None:
    response = requests.Response()
    response.status_code = 302
    response.headers["Location"] = "https://www.iworkfor.sa.gov.au/jb/page/../../not-approved/test"
    response.raw = BytesIO()
    
    with pytest.raises(expected_exception=ValueError):    
        validate_url_redirect(response)

def test_embedded_credentials() -> None:
    response = requests.Response()
    response.status_code = 302
    response.headers["Location"] = "https://testuser:testpass@www.iworkfor.sa.gov.au/jb/page/test"
    response.raw = BytesIO()
    
    with pytest.raises(expected_exception=ValueError):    
        validate_url_redirect(response)

def test_unapproved_port() -> None:
    response = requests.Response()
    response.status_code = 302
    response.headers["Location"] = "https://www.iworkfor.sa.gov.au:8443/jb/page/test"
    response.raw = BytesIO()
    
    with pytest.raises(expected_exception=ValueError):    
        validate_url_redirect(response)

def test_dot_segment_path_escape() -> None:
    response = requests.Response()
    response.status_code = 302
    response.headers["Location"] = "https://www.iworkfor.sa.gov.au/jb/page/../../not-approved/test"
    response.raw = BytesIO()
    
    with pytest.raises(expected_exception=ValueError):    
        validate_url_redirect(response)

def test_validate_url_redirect_rejects_oversized_response() -> None:
    response = requests.Response()
    response.status_code = 302
    response.headers["Location"] = "/jb/page/test"
    response.raw = BytesIO(initial_bytes=b"x" * (MAX_RESPONSE_SIZE + 1))

    with pytest.raises(expected_exception=ValueError):
        validate_url_redirect(response)