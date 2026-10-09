import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
from urllib.parse import urlparse
import json
from pathlib import Path
from datetime import datetime, timezone
import uuid
import time

sites = {
    "i_work_for_sa": {
        "base_url": "https://www.iworkfor.sa.gov.au",
        "job_search_url": "https://www.iworkfor.sa.gov.au/jb/page/page.php?pageID=842&windowUID=0",
    }
}

MAX_RESPONSE_SIZE = 5242880
MIN_REQUEST_INTERVAL = 2

def fetch_job_listings_html():
    with requests.Session() as session:
        session.headers.update({"User-Agent": "BurrowScout/0.1.0 (Python; wage-data research)"})
        timeout = (5, 30)
        start_time = time.monotonic()
        response = session.get(sites["i_work_for_sa"]["job_search_url"], timeout=timeout, allow_redirects=False) #Later Stream=True needs to be implemented as well as a new limiting operation
        if response.status_code != 200:
            raise ValueError(f"Failed to fetch the job search page. Status code: {response.status_code}")
        if len(response.content) > MAX_RESPONSE_SIZE:
            raise ValueError (f"{len(response.content)} exceeds max limit.")
        content_type = response.headers.get("Content-Type")
        cleaned_content_type = content_type.split(";")[0].strip().lower() if content_type else ""
        if cleaned_content_type != "text/html":
            raise ValueError(f"Unexpected content type: {cleaned_content_type}")
        soup = BeautifulSoup(response.content, "html.parser")
        jobtoken = soup.find("input", attrs={"name": "jobboard_token"})
        jobtoken_value = jobtoken["value"] if jobtoken else None
        if jobtoken_value is None:
            raise ValueError("Job token not found.")
        elapsed_time = (time.monotonic() - start_time)
        if elapsed_time < MIN_REQUEST_INTERVAL:
            time.sleep(MIN_REQUEST_INTERVAL - elapsed_time)
        post_start = time.monotonic()
        response_post = session.post(sites["i_work_for_sa"]["job_search_url"], data={"jobboard_token": jobtoken_value, "action": "Search", "c_179[]": [40480]}, timeout=timeout, allow_redirects=False)
        if response_post.status_code != 302:
            raise ValueError(f"Failed to submit the job search form. Status code: {response_post.status_code}")
        location_header = response_post.headers.get("Location")
        if location_header is None:
            raise ValueError("Redirect response did not contain a Location header.")
        make_absolute = urljoin(sites["i_work_for_sa"]["base_url"], location_header)
        approved_hostname = urlparse(sites["i_work_for_sa"]["base_url"]).hostname
        parsed_url_redirect = urlparse(make_absolute)
        if parsed_url_redirect.scheme != "https":
            raise ValueError("Redirect used an unapproved scheme")
        if parsed_url_redirect.hostname != approved_hostname:
            raise ValueError("Redirect used an unapproved hostname")
        if not parsed_url_redirect.path.startswith("/jb/page/"):
            raise ValueError("Redirect used an unapproved path")
        second_elapsed_time = (time.monotonic() - post_start)
        if second_elapsed_time < MIN_REQUEST_INTERVAL:
            time.sleep(MIN_REQUEST_INTERVAL - second_elapsed_time)
        final_response = session.get(make_absolute, timeout=timeout ,allow_redirects=False)
        if final_response.status_code != 200:
            raise ValueError(f"Validate Redirect Target returned unexpected status. Status code {final_response.status_code} ")
        if len(final_response.content) > MAX_RESPONSE_SIZE:
            raise ValueError (f"{len(final_response.content)} exceeds max limit.")
        content_type = final_response.headers.get("Content-Type")
        cleaned_content_type = content_type.split(";")[0].strip().lower() if content_type else ""
        if cleaned_content_type != "text/html":
            raise ValueError(f"Unexpected content type: {cleaned_content_type}")
        return final_response.content

    
def parse_content(html_content):     
    new_soup = BeautifulSoup(html_content, "html.parser")
    if new_soup.select_one("#brs_report_table_16") is None:
        raise ValueError("Job listings table not found in the response.")
    table_content = new_soup.select("#brs_report_table_16 tr.evenrow, #brs_report_table_16 tr.oddrow")
    if not table_content: # Needs to be fixed in later update to not treat 0 results as an error
        raise ValueError("No job listings found in the table.")
    jobs = []
    required_fields = ["job_title", "job_reference_number", "job_posting_date", "job_classification", "job_salary", "job_location"]
    optional_fields = ["job_closing_date", "job_agency", "job_link"]
    for row in table_content:
        cells = row.find_all("td")
        if len(cells) != 8:
            raise ValueError(f"Unexpected number of columns in the job listing row. Expected 8, but found {len(cells)}.")
        job = {
                "job_title": cells[0].get_text(separator=" ", strip=True),
                "job_reference_number": cells[1].get_text(strip=True),
                "job_posting_date": cells[2].get_text(strip=True),
                "job_closing_date": cells[3].get_text(strip=True),
                "job_agency": cells[4].get_text(strip=True),
                "job_classification": cells[5].get_text(separator=" | ", strip=True),
                "job_salary": cells[6].get_text(separator=" ",strip=True),
                "job_location": cells[7].get_text(strip=True)
            }
        job["job_link"] = None  # Initialize job_link to None
        link = cells[0].find("a")
        if link:
            cleaned_job_title = link.get_text(separator=" ",strip=True)
            job["job_title"] = cleaned_job_title
            job_link = link.get("href")
            if job_link:
                job["job_link"] = urljoin(sites["i_work_for_sa"]["base_url"], job_link)
        for field in required_fields:
            if not job[field]:
                raise ValueError(f"Missing required field '{field}' in job listing: {job['job_title']}")
        for field in optional_fields:
            if not job[field]:
                job[field] = None
        jobs.append(job)
    return jobs

def create_run_uuid():
    job_run_id = uuid.uuid4()
    return str(job_run_id)

def create_run_metadata(jobs, job_run_id):
    metadata = {
        "source": 'i_work_for_sa',
        "source_url": sites['i_work_for_sa']['job_search_url'],
        "observed_at_utc": datetime.now(timezone.utc).isoformat(),
        "record_count": len(jobs),
        "run_id": job_run_id
    }
    return metadata
    
def create_output_directory():
    output_dir = Path("data") / "i_work_for_sa"
    output_dir.mkdir(parents=True, exist_ok=True)
    return output_dir 

def create_new_dict_with_metadata(jobs, metadata):
    output = {
        "metadata": metadata,
        "jobs": jobs
    }
    return output

def save_output_to_file(output, run_timestamp, job_run_id):
    output_dir = create_output_directory()
    output_file = output_dir / f"jobs_{job_run_id}_{run_timestamp}.json"
    with open(output_file, "x", encoding="utf-8") as f:
        json.dump(output, f, indent=4)

def main():  # Call the main function to execute the script
    html_content = fetch_job_listings_html()
    jobs = parse_content(html_content=html_content)
    run_timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    job_run_uuid = create_run_uuid()
    metadata = create_run_metadata(jobs, job_run_uuid)
    jobs_dict = create_new_dict_with_metadata(jobs, metadata)
    save_output_to_file(jobs_dict, run_timestamp, job_run_uuid)

if __name__ == "__main__":
    main()