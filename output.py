from pathlib import Path
from datetime import timezone, datetime
from typing import Any
import uuid
from config import sites
import json

def create_run_uuid() -> str:
    job_run_id: uuid.UUID = uuid.uuid7()
    return str(object=job_run_id)

def create_run_metadata(jobs: list[Any], job_run_id: str) -> dict[str, str | int | Any]:
    metadata: dict[str, str | int] = {
        "source": 'i_work_for_sa',
        "source_url": sites['i_work_for_sa']['job_search_url'],
        "observed_at_utc": datetime.now(tz=timezone.utc).isoformat(),
        "record_count": len(jobs),
        "run_id": job_run_id
    }
    return metadata
    
def create_output_directory() -> Path:
    output_dir: Path = Path("data") / "i_work_for_sa"
    output_dir.mkdir(parents=True, exist_ok=True)
    return output_dir 

def create_new_dict_with_metadata(jobs: list[Any], metadata: dict[str, str | int | Any]) -> dict[str, Any]:
    output: dict[str, Any] = {
        "metadata": metadata,
        "jobs": jobs
    }
    return output

def save_output_to_file(output: dict[str, Any], run_timestamp: str, job_run_id: str) -> None:
    output_dir: Path = create_output_directory()
    output_file: Path = output_dir / f"jobs_{job_run_id}_{run_timestamp}.json"
    with open(file=output_file, mode="x", encoding="utf-8") as f:
        json.dump(obj=output, fp=f, indent=4)