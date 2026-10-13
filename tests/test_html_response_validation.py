from io import BytesIO
from config import MAX_RESPONSE_SIZE
import requests
import pytest
from i_work_for_sa import validate_html_response

def test_validate_html_response_rejects_invalid_status()-> None:
    response = requests.Response()
    response.status_code = 404
    response.headers["Content-Type"] = "text/html"


    with pytest.raises(expected_exception=ValueError):
        validate_html_response(response)

def test_validate_html_response_rejects_invalid_content_type() -> None:
    response = requests.Response()
    response.status_code = 200
    response.headers["Content-Type"] = "application/json"
    response.raw = BytesIO(initial_bytes=b"<html></html>")


    with pytest.raises(expected_exception=ValueError):
        validate_html_response(response)

def test_validate_html_response_accepts_maximum_size() -> None:
    response = requests.Response()
    response.status_code = 200
    response.headers["Content-Type"] = "text/html" 
    response.raw = BytesIO(initial_bytes=b"x"*MAX_RESPONSE_SIZE)

    validate_html_response(response)

def test_validate_html_response_rejects_oversized_response() -> None:
    response = requests.Response()
    response.status_code = 200
    response.headers["Content-Type"] = "text/html" 
    response.raw = BytesIO(initial_bytes=b"x"*(MAX_RESPONSE_SIZE+1))

    with pytest.raises(expected_exception=ValueError):
        validate_html_response(response)