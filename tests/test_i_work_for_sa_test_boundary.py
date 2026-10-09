from pathlib import Path
from sites import parse_content

def test_parse_content_returns_expected_jobs():
    fixture_path = Path(__file__).parent/ "fixtures" / "i_work_for_sa_text_boundaries.html"
    fixture_html = fixture_path.read_bytes()
    jobs = parse_content(fixture_html)

    assert len(jobs) == 1
    assert jobs[0]["job_title"] == "Finance Officer"
    assert jobs[0]["job_salary"] == "$70k - $89k per annum"
    assert jobs[0]["job_link"] == "https://www.iworkfor.sa.gov.au/jb/page/test-boundary"
