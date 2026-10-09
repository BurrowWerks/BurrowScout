# BurrowScout

BurrowScout is a Python-based data collection project for retrieving, validating,
cleaning, and storing permitted job and wage information from approved sources.

Version 0.1.0 establishes the first complete source-specific scraper using
I WORK FOR SA.

## Status

Current development release: **0.1.0**

BurrowScout 0.1.0 supports one source and one defined search scope. Later
versions will expand reliability, data processing, multi-source support,
automation, and storage.

## Current Source

- Source: I WORK FOR SA
- Search scope: Accounting and Finance
- Source identifier: `i_work_for_sa`
- Search category value: `40480`
- Result pages processed per run: 1

## Features

BurrowScout 0.1.0:

- retrieves the I WORK FOR SA search page
- extracts the dynamic job-board token
- submits the configured job search
- validates HTTP status codes
- validates returned Content-Type
- applies a maximum response-size check
- verifies expected page structure before parsing
- extracts structured job information
- distinguishes required and optional fields
- preserves original salary wording
- converts relative job links to absolute URLs
- records source and observation metadata
- writes UTF-8 JSON output
- includes an offline HTML fixture test using pytest

## Extracted Fields

Each job record contains:

- `job_title`
- `job_reference_number`
- `job_posting_date`
- `job_closing_date`
- `job_agency`
- `job_classification`
- `job_salary`
- `job_location`
- `job_link`

Required fields:

- job title
- reference number
- posting date
- classification
- salary
- location

Optional fields are represented as `null` in JSON when unavailable.

## Output Format

Each run creates a JSON document containing run metadata and collected jobs.

Example structure:

```json
{
    "metadata": {
        "source": "i_work_for_sa",
        "source_url": "https://www.iworkfor.sa.gov.au/...",
        "observed_at_utc": "2026-10-08T20:21:41+00:00",
        "record_count": 15
    },
    "jobs": []
}

## Requirements

- Python 3.11+
- requests
- beautifulsoup4
- pytest


## Installation

Clone the repository and enter the project directory.

Create a virtual environment:

```bash
python -m venv .venv
```
