from pathlib import Path
import pytest
from i_work_for_sa import parse_content

def test_parse_content_returns_expected_jobs() -> None:
    fixture_path: Path = Path(__file__).parent/ "fixtures" / "i_work_for_sa.html"
    fixture_html: bytes = fixture_path.read_bytes()
    jobs: list[dict[str, str | None]] = parse_content(html_content=fixture_html)

    assert len(jobs) == 2
    assert jobs[0]["job_title"] == "Fixture Test Officer"
    assert jobs[0]["job_salary"] == "$67,589 - $72,033"
    assert jobs[0]["job_link"] == "https://www.iworkfor.sa.gov.au/jb/page/test-job-001"
    assert jobs[0]["job_classification"] == "ASO3"
    assert jobs[1]["job_title"] == "Senior Fixture Analyst"
    assert jobs[1]["job_salary"] == "$90k - $109k, $110k - $149k"
    assert jobs[1]["job_link"] is None
    assert jobs[1]["job_closing_date"] is None
    assert jobs[1]["job_agency"] is None
    assert jobs[1]["job_classification"] == "ASO5 | ASO6"


def test_parse_content_rejects_missing_table() -> None:
    html_string: bytes = b"<html><div> something </div></html>"

    with pytest.raises(expected_exception=ValueError):
        parse_content(html_content=html_string)

def test_parse_content_rejects_missing_required_field() -> None:
    fixture_path: Path = Path(__file__).parent / "fixtures" / "i_work_for_sa.html"
    fixture_html: bytes = fixture_path.read_bytes()
    invalid_html: bytes = fixture_html.replace(b"Fixture Test Officer",
                                        b"   ",
                                        1)

    assert invalid_html != fixture_html

    with pytest.raises(expected_exception=ValueError):
        parse_content(html_content=invalid_html)

def test_parse_content_rejects_invalid_column_count() -> None:
    fixture_path: Path = Path(__file__).parent / "fixtures" / "i_work_for_sa.html"
    fixture_html: bytes = fixture_path.read_bytes()
    invalid_html: bytes = fixture_html.replace(b"<td>",
                                               b"<td>Extra</td><td>", 
                                               1)

    assert invalid_html != fixture_html

    with pytest.raises(expected_exception=ValueError):
        parse_content(html_content=invalid_html)