# BurrowScout

BurrowScout is a Python project for retrieving, validating, cleaning, and saving
job and wage information from sources reviewed for the intended collection use.
Version **0.1.0** implements a bounded, source-specific scraper for I WORK FOR SA.

## Status and scope

**Milestone:** 0.1.0 — core scraper. The implementation has passed the recorded
offline regression suite; release tagging remains subject to the final
repository and acceptance-evidence check.

| Setting | 0.1.0 scope |
| --- | --- |
| Source | I WORK FOR SA / Government of South Australia |
| Source ID | `i_work_for_sa` |
| Search | Accounting and Finance |
| Category ID | `40480` |
| Results pages | One per manually initiated run; no pagination |
| Output | One new local UTF-8 JSON file per run |

The reviewed source access, attribution and redirect boundaries are documented
in [SOURCE_MANIFEST.md](SOURCE_MANIFEST.md). The software licence does not, by
itself, grant permission to collect or redistribute third-party source data.

## Features

BurrowScout 0.1.0:

- Uses one HTTP session and the source's GET → GET → POST → GET search workflow,
  including extraction and submission of a dynamic `jobboard_token`.
- Sends an identifying User-Agent; uses `(5, 30)` second connection/read
  timeouts; enforces a minimum two-second interval between requests; and
  disables automatic redirects.
- Validates followed redirects against the approved HTTPS origin and `/jb/page/`
  path boundary, rejecting off-scope destinations before requesting them.
- Validates response status and HTML content type, and applies a **5 MiB
  post-download size check to each response**, including redirects. This is
  *not* a streamed hard-download limit.
- Checks the expected results table and row structure, rejects missing
  required data, and preserves absent optional fields as JSON `null`.
- Cleans layout whitespace without interpreting, converting or annualising
  source-provided salary wording. Multiple classifications remain distinct.
- Preserves source links according to the observed **absolute/root-relative**
  source URL contract. Path-relative URLs are outside the verified 0.1.0
  contract; see the source manifest.
- Records a source identifier, source search URL, UTC observation time, record
  count and run UUIDv7; writes a **new** UTF-8 JSON file without overwriting an
  existing run.
- Provides offline pytest regression checks using HTML fixtures and controlled
  fake HTTP responses.

## Collected fields

Each job record contains these keys:

| Required | Optional (`null` if absent) |
| --- | --- |
| `job_title` | `job_closing_date` |
| `job_reference_number` | `job_agency` |
| `job_posting_date` | `job_link` |
| `job_classification` | |
| `job_salary` | |
| `job_location` | |

Salary values are descriptive text from the source, **not** calculations of
legal minimum wages, annualised earnings or normalised numeric pay.

## JSON output

The JSON document has a `metadata` object and a `jobs` array. The following
**synthetic** one-record example demonstrates the structure; it is not a claim
about a live job listing:

```json
{
  "metadata": {
    "source": "i_work_for_sa",
    "source_url": "https://www.iworkfor.sa.gov.au/jb/page/page.php?pageID=842&windowUID=0",
    "observed_at_utc": "2026-10-14T00:00:00+00:00",
    "record_count": 1,
    "run_id": "0199abcd-1234-7abc-8abc-123456789abc"
  },
  "jobs": [
    {
      "job_title": "Example Position",
      "job_reference_number": "EXAMPLE-001",
      "job_posting_date": "14 October 2026",
      "job_closing_date": null,
      "job_agency": null,
      "job_classification": "ASO3",
      "job_salary": "$70k - $89k",
      "job_location": "ADELAIDE",
      "job_link": null
    }
  ]
}
```

Runtime files are written under `data/i_work_for_sa/` and are **not intended
for Git tracking**. The curated representative release sample is documented
at [examples/i_work_for_sa_sample.json](examples/i_work_for_sa_sample.json);
keep it separate from generated runtime output. Metadata `record_count` reflects
the jobs recorded in that run; it is not a claim about all jobs on the website.

## Requirements and installation

- Python **3.14 or later**
- `requests` and `beautifulsoup4` (runtime dependencies)
- `pytest` (testing)

Use the pinned development/test dependencies in `requirements.txt`.
For example, from the project root on **Ubuntu/WSL**:

```bash
python -m venv .venv-wsl
source .venv-wsl/bin/activate
python -m pip install -r requirements.txt
python -m pytest -v
python main.py
```

For **Windows PowerShell**, full activation commands, and troubleshooting, see
[RUN_INSTRUCTIONS.md](RUN_INSTRUCTIONS.md). Run the commands from the project
root. `python main.py` performs a **live** source request; the pytest suite uses
offline fixtures and fakes. Review the source conditions before live use.

## Verification and release evidence

The reported WSL/Linux verification on **14 October 2026** used Python
**3.14.4**, pytest **9.1.1**, and produced **32 passed** in **0.82 seconds**.
That test result covers the 0.1.0 regression gate, including a simulated
four-request workflow, request-spacing checks, encoded redirect-traversal
rejection, real UUIDv7 generation through `main()` and release-sample JSON
validation. It is not itself a live
website availability check or proof of release sign-off.

For the manually inspected 11 October source comparison (one results page,
14 records, three checked job listings and their links), see
[docs/0.1.0-live-verification.md](docs/0.1.0-live-verification.md).
See also [CHANGELOG.md](CHANGELOG.md) for the release history and final gate.
The separate earlier collection described in the changelog is not the
14-record representative sample.

## Limits and future work

0.1.0 supports only one source/category and one page, with manual execution.
A genuine zero-result table is currently treated as an error; there is no
pagination, retry system, scheduling, database, deduplication or historical
comparison. The response limit is enforced after downloading, not while
streaming. These are documented limitations, not missing 0.1.0 features.

See [KNOWN_LIMITATIONS.md](KNOWN_LIMITATIONS.md) for details and the
[design roadmap](BurrowScout-Design-Architecture-Build-Roadmap-D01-Updated.md)
for later-version plans.

## Licence and attribution

BurrowScout's code is distributed under the repository's MIT `LICENSE.txt`.
Content obtained from I WORK FOR SA remains subject to its applicable
attribution, licensing and third-party conditions; see
[SOURCE_MANIFEST.md](SOURCE_MANIFEST.md).
