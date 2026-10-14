# BurrowScout 0.1.0 — Run instructions

BurrowScout requires **Python 3.14+**. Run commands from the **project root**.

**Recorded tested environment (14 October 2026):** WSL/Linux, Python 3.14.4,
pytest 9.1.1. The offline suite recorded **32 passed in 0.82 seconds**.
The PowerShell instructions below are provided for use on Windows but do not
assert that a separate Windows release test has been completed.

## Before a live run

Review [SOURCE_MANIFEST.md](SOURCE_MANIFEST.md) for the source's approved
collection scope, attribution and request policy. 0.1.0 requests only one
results page for the configured I WORK FOR SA Accounting and Finance category
(`40480`). The command `python main.py` accesses the live source; the pytest
suite is offline.

## Ubuntu / WSL

Open WSL and change into your BurrowScout checkout:

```bash
cd /path/to/BurrowScout
python -m venv .venv-wsl
source .venv-wsl/bin/activate
python -m pip install -r requirements.txt
```

The `/path/to/BurrowScout` path is illustrative; substitute your actual
checkout. Windows and WSL must use **separate** virtual environments.

### Run offline regression tests

```bash
python -m pytest -v
```

The tests use synthetic HTML in `tests/fixtures/` and controlled fake HTTP
responses; they do not require the live website. The recorded 0.1.0 suite has
32 passing tests, covering parser boundaries, redirect safety (including
encoded path traversal), response-size limits, JSON writing, the timed
four-request workflow and end-to-end UUIDv7 output generation.

### Collect one live results page

```bash
python main.py
```

On success the program fetches, validates and parses the configured source,
then writes a **new** JSON file under:

```text
data/i_work_for_sa/
```

The run is manual and limited to one results page. Check the output for a
`metadata` object and `jobs` array, including source URL, UTC observation
time, run UUID and `record_count`. Confirm that `record_count` equals the number
of saved job entries. Each run is written to a separate file; an existing
identical filename is not overwritten.

### Deactivate

```bash
deactivate
```

## Windows PowerShell

From the project root in PowerShell (the following path is illustrative):

```powershell
cd C:\path\to\BurrowScout
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
python -m pytest -v
python main.py
```

If your environment blocks activation, review PowerShell's execution-policy
requirements; do not disable security controls permanently just to run the
project. Deactivate afterwards with `deactivate`.

Do not reuse a Windows `.venv` inside WSL or a WSL `.venv-wsl` inside Windows.
The documented verified test result is from **WSL/Linux**, not a separate
Windows test matrix.

## 0.1.0 acceptance and release checks

For the release demonstration, use a small, **permitted** live run and retain
its output filename/run ID, source/category, date, observed results-page count,
and a comparison of **two** records' title/classification, salary wording and
links against the source. Also confirm the fixture case with missing optional
fields yields JSON `null`. Retain this evidence with the release record; do
not infer the full website's listing count from the single retrieved page.
The retained 11 October verification record is
[docs/0.1.0-live-verification.md](docs/0.1.0-live-verification.md).

Before tagging 0.1.0:

1. Run `python -m pytest -v` and review all results.
2. Confirm the curated `examples/i_work_for_sa_sample.json` exists and is
   deliberately tracked; keep generated `data/` output untracked.
3. Verify the Git ignore rules and existing tracked files from the repo root:

   ```bash
   git check-ignore -v data/i_work_for_sa/jobs_example.json .venv-wsl/bin/python
   git ls-files -- data/ .venv-wsl/
   git status --short
   ```

   `git check-ignore` verifies the new rules (the candidate paths need not
   exist); `git ls-files` should produce no unintended tracked runtime files.
   **An ignore rule does not untrack files already in Git's index.** Review
   any existing tracked data before removing it from the index; retain curated
   examples and `tests/fixtures/` deliberately.
4. Review [CHANGELOG.md](CHANGELOG.md), [KNOWN_LIMITATIONS.md](KNOWN_LIMITATIONS.md),
   the source manifest and the
   [live acceptance evidence](docs/0.1.0-live-verification.md) together.
   Tag 0.1.0 only after the acceptance gate is satisfied.

## Operational notes

- The adapter uses four HTTP requests in a fixed GET → GET → POST → GET flow,
  with two approved redirects; it disables automatic redirect following.
- It uses two-second minimum request spacing and `(5, 30)` second
  connection/read timeouts.
- A response larger than **5 MiB** is rejected **after download**, including
  redirect responses. A streamed hard limit is deferred to 0.2.0.
- Unexpected HTTP statuses, content types, structure changes or missing
  required fields cause failure rather than a fabricated empty success.
- BurrowScout 0.1.0 has no retries or scheduler. Failures should be inspected
  rather than bypassing the documented source boundaries.
