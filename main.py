from datetime import datetime
from i_work_for_sa import fetch_job_listings_html, parse_content
from output import create_run_uuid, create_run_metadata, create_new_dict_with_metadata, save_output_to_file

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