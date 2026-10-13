sites: dict[str, dict[str, str | int]] = {
    "i_work_for_sa": {
        "base_url": "https://www.iworkfor.sa.gov.au",
        "job_search_url": "https://www.iworkfor.sa.gov.au/jb/page/page.php?pageID=842&windowUID=0",
        "category_id": 40480,
    }
}

MAX_RESPONSE_SIZE = 5242880
MIN_REQUEST_INTERVAL = 2
USER_AGENT: dict[str, str] = {"User-Agent": "BurrowScout/0.1.0 (Python; wage-data research)"}
REQUEST_TIMEOUT = (5, 30)