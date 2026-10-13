from datetime import datetime
from typing import Any
from i_work_for_sa import fetch_job_listings_html, parse_content
from output import create_run_uuid, create_run_metadata, create_new_dict_with_metadata, save_output_to_file

def main() -> None:  # Call the main function to execute the script
    html_content: bytes = fetch_job_listings_html()
    jobs: list[dict[str, str | None]] = parse_content(html_content=html_content)
    run_timestamp: str = datetime.now().strftime(format="%Y-%m-%d_%H-%M-%S")
    job_run_uuid: str = create_run_uuid()
    metadata: dict[str, str | int | Any] = create_run_metadata(jobs, job_run_id=job_run_uuid)
    jobs_dict: dict[str, Any] = create_new_dict_with_metadata(jobs, metadata)
    save_output_to_file(output=jobs_dict, run_timestamp=run_timestamp, job_run_id=job_run_uuid)

if __name__ == "__main__":
    main()