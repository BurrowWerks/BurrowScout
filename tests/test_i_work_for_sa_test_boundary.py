from pathlib import Path
from typing import Any, Callable, cast
from i_work_for_sa import parse_content as _parse_content

parse_content: Callable[[bytes], list[dict[str, Any]]] = cast(
    Callable[[bytes], list[dict[str, Any]]], _parse_content
)

def test_parse_content_returns_expected_jobs() -> None:
    fixture_path: Path = Path(__file__).parent/ "fixtures" / "i_work_for_sa_text_boundaries.html"
    fixture_html: bytes = fixture_path.read_bytes()
    jobs: list[Any] = parse_content(fixture_html)

    assert len(jobs) == 1
    assert jobs[0]["job_title"] == "Finance Officer"
    assert jobs[0]["job_salary"] == "$70k - $89k per annum"
    assert jobs[0]["job_link"] == "https://www.iworkfor.sa.gov.au/jb/page/test-boundary"
    assert jobs[0]["job_agency"] == "Department of Testing"
    assert jobs[0]["job_location"] == "Metropolitan Adelaide"
