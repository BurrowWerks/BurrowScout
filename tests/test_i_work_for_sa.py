from pathlib import Path
from sites import parse_content

def test_parse_content_returns_expected_jobs():
    fixture_path = Path(__file__).parent/ "fixtures" / "i_work_for_sa.html"
    fixture_html = fixture_path.read_bytes()
    jobs = parse_content(fixture_html)

    assert len(jobs) == 2
    assert jobs[0]["job_title"] == "Fixture Test Officer"
    assert jobs[0]["job_salary"] == "$67,589 - $72,033"
    assert jobs[0]["job_link"] == "https://www.iworkfor.sa.gov.au/jb/page/test-job-001"
    assert jobs[1]["job_closing_date"] is None
    assert jobs[1]["job_agency"] is None
    assert jobs[1]["job_classification"] == "ASO5 | ASO6"