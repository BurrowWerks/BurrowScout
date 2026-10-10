import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
from urllib.parse import urlparse
import time
from config import sites, MAX_RESPONSE_SIZE, MIN_REQUEST_INTERVAL, REQUEST_TIMEOUT, USER_AGENT

def fetch_job_listings_html():
    with requests.Session() as session:
        session.headers.update(USER_AGENT)
        start_time = time.monotonic()
        initial_response = session.get(sites["i_work_for_sa"]["job_search_url"],
                                        timeout=REQUEST_TIMEOUT, allow_redirects=False)
                                        #Later Stream=True needs to be implemented as well as a new limiting operation
        initial_redirect_url = validate_url_redirect(initial_response)
        
        wait_for_request_interval(start_time)
        
        second_get_start_time = time.monotonic()
        search_page_response = session.get(initial_redirect_url,
                                            timeout=REQUEST_TIMEOUT,
                                            allow_redirects=False)
        validate_html_response(search_page_response)
        jobtoken_value = extract_jobboard_token(search_page_response)
        
        wait_for_request_interval(second_get_start_time)
        
        post_start = time.monotonic()
        search_response_post = session.post(sites["i_work_for_sa"]["job_search_url"], 
                                            data={"jobboard_token": jobtoken_value,
                                                   "action": "Search",
                                                    "c_179[]": sites["i_work_for_sa"]["category_id"] },
                                              timeout=REQUEST_TIMEOUT, allow_redirects=False)
        results_redirect_url = validate_url_redirect(search_response_post)
        
        wait_for_request_interval(post_start)
        
        results_response = session.get(results_redirect_url, 
                                        timeout=REQUEST_TIMEOUT,
                                        allow_redirects=False)
        validate_html_response(results_response)    
        
        return results_response.content

def validate_html_response(response):
    content_type = response.headers.get("Content-Type")
    cleaned_content_type = content_type.split(";")[0].strip().lower() if content_type else ""
    if response.status_code != 200:
        raise ValueError(f"HTML response returned unexpected status. Status code: {response.status_code}")
    if len(response.content) > MAX_RESPONSE_SIZE:
        raise ValueError (f"{len(response.content)} exceeds max limit.")
    if cleaned_content_type != "text/html":
        raise ValueError(f"Unexpected content type: {cleaned_content_type}")

def extract_jobboard_token(response):
    soup = BeautifulSoup(response.content, "html.parser")
    jobtoken = soup.find("input", attrs={"name": "jobboard_token"})
    jobtoken_value = jobtoken["value"] if jobtoken else None        
    if jobtoken_value is None:
        raise ValueError("Job token not found.")
    return jobtoken_value

def wait_for_request_interval(start_time):
    elapsed_time = (time.monotonic() - start_time)
    if elapsed_time < MIN_REQUEST_INTERVAL:
        time.sleep(MIN_REQUEST_INTERVAL - elapsed_time)

def validate_url_redirect(response):
    if response.status_code != 302:
        raise ValueError(f"Expected redirect response, received status code: {response.status_code}")    
    location_header = response.headers.get("Location")
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
    return make_absolute
    
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

