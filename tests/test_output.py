from config import sites
from output import create_run_metadata, save_output_to_file
from datetime import timedelta, datetime
from pathlib import Path
import pytest
import json

def test_create_run_metadata() -> None:
    job: list[dict[str, str]] = [
        {
            "job_title": "job title",
            "date": "Now",
            
        },
        {
            "job_two_title": "job title",
            "date": "Yesterday",
        },
    ]

    run_id = "ABCDEFG"

    metadata: dict[str, str | int] = create_run_metadata(job,run_id)
    timestamp: str | int = metadata["observed_at_utc"]


    assert metadata["record_count"] == 2
    assert metadata["run_id"] == "ABCDEFG"
    assert metadata["source"] == "i_work_for_sa"
    assert metadata["source_url"] == sites["i_work_for_sa"]["job_search_url"]
    assert isinstance(timestamp, str)
    parsed_timestamp = datetime.fromisoformat(timestamp)
    assert parsed_timestamp.utcoffset() == timedelta(0)

def test_save_output_round_trip(tmp_path: Path,monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.chdir(tmp_path)
    new_dict = {"metadata":
                {"source": 
                "i_work_for_sa"},
                "jobs": [{"job_title": 
                        "Tester",
                        "job_salary": "$90k"}]}
    run_timestamp = "2026-10-13_15-00-00"
    job_run_id = "TEST123"

    save_output_to_file(new_dict, run_timestamp, job_run_id)

    output_file = tmp_path/"data"/"i_work_for_sa"/f"jobs_{job_run_id}_{run_timestamp}.json"
    
    
    assert output_file.is_file()

    with open(output_file, "r", encoding="utf-8") as file:
        loaded_data = json.load(file)

    assert loaded_data == new_dict

def test_save_output_prevents_overwrite(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.chdir(tmp_path)
    new_dict = {"metadata":
                {"source": 
                "i_work_for_sa"},
                "jobs": [{"job_title": 
                        "Tester",
                        "job_salary": "$90k"}]}

    run_timestamp = "2026-10-13_15-00-00"
    job_run_id = "TEST123"


    save_output_to_file(new_dict, run_timestamp, job_run_id)

    output_file = tmp_path/"data"/"i_work_for_sa"/f"jobs_{job_run_id}_{run_timestamp}.json"

    output_file_bytes = output_file.read_bytes()

    with pytest.raises(FileExistsError):
        save_output_to_file(new_dict, run_timestamp, job_run_id)

    assert output_file.read_bytes() == output_file_bytes