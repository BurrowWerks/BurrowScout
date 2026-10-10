from pathlib import Path
from datetime import timezone, datetime
import uuid
from config import sites
import json

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