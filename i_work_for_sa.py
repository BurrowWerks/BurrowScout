from bs4.element import AttributeValueList, ResultSet, Tag
import requests
from bs4 import BeautifulSoup
from urllib.parse import ParseResult, urljoin
from urllib.parse import urlparse
import time
from config import sites, MAX_RESPONSE_SIZE, MIN_REQUEST_INTERVAL, REQUEST_TIMEOUT, USER_AGENT

def fetch_job_listings_html() -> bytes:
    with requests.Session() as session:
        session.headers.update(USER_AGENT)
        start_time: float = time.monotonic()
        initial_response: requests.Response = session.get(url=str(object=sites["i_work_for_sa"]["job_search_url"]),
                                        timeout=REQUEST_TIMEOUT, allow_redirects=False)
                                        #Later Stream=True needs to be implemented as well as a new limiting operation
        initial_redirect_url: str = validate_url_redirect(response=initial_response)
        print("Initial request URL:", initial_response.url)
        print("Initial redirect Location:", initial_response.headers.get("Location"))
        
        wait_for_request_interval(start_time)
        
        second_get_start_time: float = time.monotonic()
        search_page_response: requests.Response = session.get(
            url=initial_redirect_url,
            timeout=REQUEST_TIMEOUT,
            allow_redirects=False,
        )
        validate_html_response(response=search_page_response)
        jobtoken_value: str | AttributeValueList = extract_jobboard_token(response=search_page_response)
        
        wait_for_request_interval(start_time=second_get_start_time)
        
        post_start: float = time.monotonic()
        search_response_post: requests.Response = session.post(
            url=str(object=sites["i_work_for_sa"]["job_search_url"]),
            data={
                "jobboard_token": jobtoken_value,
                "action": "Search",
                "c_179[]": sites["i_work_for_sa"]["category_id"],
            },
            timeout=REQUEST_TIMEOUT,
            allow_redirects=False,
        )
        results_redirect_url: str = validate_url_redirect(response=search_response_post)
        print("POST request URL:", search_response_post.url)
        print("POST redirect Location:", search_response_post.headers.get("Location"))
        
        wait_for_request_interval(start_time=post_start)
        
        results_response: requests.Response = session.get(results_redirect_url, 
                                        timeout=REQUEST_TIMEOUT,
                                        allow_redirects=False)
        validate_html_response(response=results_response)    
        
        return results_response.content


def validate_response_size(response: requests.Response) -> None:
    if len(response.content) > MAX_RESPONSE_SIZE:
        raise ValueError(f"{len(response.content)} exceeds max limit.")

def validate_html_response(response: requests.Response) -> None:
    content_type: str | None = response.headers.get("Content-Type")
    cleaned_content_type: str = content_type.split(sep=";")[0].strip().lower() if content_type else ""
    if response.status_code != 200:
        raise ValueError(f"HTML response returned unexpected status. Status code: {response.status_code}")
    validate_response_size(response)
    if cleaned_content_type != "text/html":
        raise ValueError(f"Unexpected content type: {cleaned_content_type}")

def extract_jobboard_token(response: requests.Response) -> str | AttributeValueList:
    soup = BeautifulSoup(markup=response.content, features="html.parser")
    jobtoken: Tag | None = soup.find(name="input", attrs={"name": "jobboard_token"})
    jobtoken_value: str | AttributeValueList | None = jobtoken["value"] if jobtoken else None        
    if jobtoken_value is None:
        raise ValueError("Job token not found.")
    return jobtoken_value

def wait_for_request_interval(start_time: float) -> None:
    elapsed_time: float = (time.monotonic() - start_time)
    if elapsed_time < MIN_REQUEST_INTERVAL:
        time.sleep(MIN_REQUEST_INTERVAL - elapsed_time)

def validate_url_redirect(response: requests.Response) -> str:
    if response.status_code != 302:
        raise ValueError(f"Expected redirect response, received status code: {response.status_code}")
    validate_response_size(response)   
    location_header: str | None = response.headers.get("Location")
    if location_header is None:
        raise ValueError("Redirect response did not contain a Location header.")
    base_url_raw: str | int = sites["i_work_for_sa"]["base_url"]
    if not isinstance(base_url_raw, str):
        raise TypeError("Base URL must be a string.")
    make_absolute: str = urljoin(base=base_url_raw, url=location_header)
    prepared_url: str | None = requests.Request(method="GET", url=make_absolute).prepare().url
    if prepared_url is None:
        raise ValueError("Redirect URL could not be prepared.")
    approved_hostname: str | None = urlparse(url=base_url_raw).hostname
    if approved_hostname is None:
        raise ValueError("Base URL did not contain a valid hostname.")
    parsed_url_redirect: ParseResult = urlparse(url=prepared_url)
    if parsed_url_redirect.username is not None or parsed_url_redirect.password is not None:
        raise ValueError("Redirect contained embedded credentials")
    if parsed_url_redirect.scheme != "https":
        raise ValueError("Redirect used an unapproved scheme")
    if parsed_url_redirect.port not in (None, 443):
        raise ValueError("Redirect used an unapproved port.")
    if parsed_url_redirect.hostname != approved_hostname:
        raise ValueError("Redirect used an unapproved hostname")
    if not parsed_url_redirect.path.startswith("/jb/page/"):
        raise ValueError("Redirect used an unapproved path")
    return prepared_url

def clean_extracted_text(text: str) -> str:
        remove_whitespace: list[str] = text.split()
        join_text: str = " ".join(remove_whitespace)
        return join_text
    
def parse_content(html_content: bytes) -> list[dict[str, str | None]]:     
    new_soup = BeautifulSoup(markup=html_content, features="html.parser")
    if new_soup.select_one(selector="#brs_report_table_16") is None:
        raise ValueError("Job listings table not found in the response.")
    table_content: ResultSet[Tag] = new_soup.select(selector="#brs_report_table_16 tr.evenrow, #brs_report_table_16 tr.oddrow")
    if not table_content: # Needs to be fixed in later update to not treat 0 results as an error
        raise ValueError("No job listings found in the table.")
    jobs: list[dict[str, str | None]] = []
    required_fields: list[str] = ["job_title", "job_reference_number", "job_posting_date", "job_classification", "job_salary", "job_location"]
    optional_fields: list[str] = ["job_closing_date", "job_agency", "job_link"]
    for row in table_content:
        cells: ResultSet[Tag] = row.find_all(name="td")
        if len(cells) != 8:
            raise ValueError(f"Unexpected number of columns in the job listing row. Expected 8, but found {len(cells)}.")
        job: dict[str, str | None] = {
                "job_title": clean_extracted_text(text=cells[0].get_text(separator=" ", strip=True)),
                "job_reference_number": clean_extracted_text(text=cells[1].get_text(separator=" ", strip=True)),
                "job_posting_date": clean_extracted_text(text=cells[2].get_text(separator=" ",strip=True)),
                "job_closing_date": clean_extracted_text(text=cells[3].get_text(separator=" ",strip=True)),
                "job_agency": clean_extracted_text(text=cells[4].get_text(separator=" ", strip=True)),
                "job_classification": clean_extracted_text(text=cells[5].get_text(separator=" | ", strip=True)),
                "job_salary": clean_extracted_text(text=cells[6].get_text(separator=" ",strip=True)),
                "job_location": clean_extracted_text(text=cells[7].get_text(separator=" ",strip=True))
            }

        job["job_link"] = None  # Initialize job_link to None
        link: Tag | None = cells[0].find(name="a")
        if link:
            cleaned_job_title: str = clean_extracted_text(text=link.get_text(separator=" ",strip=True))
            job["job_title"] = cleaned_job_title
            job_link: str | AttributeValueList | None = link.get(key="href")
            print("Raw job href:", job_link)
            if job_link:
                if not isinstance(job_link, str):
                    raise TypeError("Job link must be a string.")
                base_url: str | int = sites["i_work_for_sa"]["base_url"]
                if not isinstance(base_url, str):
                    raise TypeError("Base URL must be a string.")
                job["job_link"] = urljoin(base=base_url, url=job_link)
        for field in required_fields:
            if not job[field]:
                raise ValueError(f"Missing required field '{field}' in job listing: {job['job_title']}")
        for field in optional_fields:
            if not job[field]:
                job[field] = None
        jobs.append(job)
    return jobs

