# Changelog

Notable BurrowScout changes and milestone verification are recorded here.
Dates refer to recorded work or test evidence, **not** an assertion that a
Git tag or public release has been published.

## 0.1.0 — Core Scraper

**Verification updated:** 14 October 2026  
**Release state:** implementation and offline regression testing complete.
The Git ignore/index checks and live-evidence confirmations have been
reported as passing; final release commit and sign-off remain before tagging.

### Delivered scope

- I WORK FOR SA adapter for the **Accounting and Finance** category (`40480`),
  processing **one results page** per manually initiated run.
- Bounded GET → GET → POST → GET session workflow with dynamic job-board token,
  truthful User-Agent, connection/read timeouts and minimum request spacing.
- Explicit validation of HTTPS redirect destinations within the approved
  origin/path, automatic redirects disabled, HTTP status and content-type
  checks, and a post-download **5 MiB check on every HTTP response**.
- Expected-table/row and required-field validation; optional fields recorded
  as JSON `null`; whitespace cleanup preserving salary meaning and separate
  classification labels.
- Observed root-relative and absolute link forms handled according to the
  [source manifest](SOURCE_MANIFEST.md); path-relative forms are outside the
  verified 0.1.0 source contract.
- Local UTF-8 JSON outputs containing source ID, full source URL, UTC
  observation timestamp, record count, run UUID and job records. Output uses
  new files and does not overwrite an existing run. Python **3.14+** is
  required for the standard-library UUIDv7 generator.
- Pinned development dependencies, setup/run instructions, known-limitations
  note, synthetic fixtures, example output and offline regression tests.

### Verification and evidence

- **Offline regression run (14 October 2026):** `python -m pytest -v` under
  **WSL/Linux, Python 3.14.4, pytest 9.1.1** — **32 passed in 0.82 seconds**
  (latest user-reported full-suite result). The tests include the controlled
  four-request workflow, request options and spacing, response validation,
  parser/output boundaries, and two forms of encoded redirect traversal with
  assertions that the unsafe redirect is not requested.
- **Application-level UUIDv7 check:** an offline test executes the real
  `main()` flow with a valid HTML fixture and controlled HTTP responses, writes
  output in a pytest temporary directory, then checks the saved run ID is
  UUID version 7. The real UUID generator was not mocked.
- **Representative release sample:**
  [examples/i_work_for_sa_sample.json](examples/i_work_for_sa_sample.json) is
  the curated **14-job** JSON from **11 October 2026**, run ID
  `f0178939-d4f7-4dc8-8999-9f8fbd451ea7`, observation timestamp
  `2026-10-11T03:40:22.483838+00:00`. The entire corrected sample is valid
  JSON; a regression test confirms the 14 records match the metadata count.
  This is a historical run and retains its original UUID rather than
  presenting it as a newly generated UUIDv7 run.
- **Live verification:** see
  [docs/0.1.0-live-verification.md](docs/0.1.0-live-verification.md) for the
  11 October **Accounting and Finance / category 40480 / one-page** comparison,
  the saved sample and three manually checked records: references `825882`,
  `860179` and `858919`. The original notes record title, reference, agency,
  classification, salary and location checks. On 14 October, the person who
  performed the comparison confirmed that each job link led to its matching
  listing and that the 11 October collection command was `python main.py`.
  These confirmations are retrospective, not a new live-source audit.
- **Separate earlier evidence:** an earlier **15-job** I WORK FOR SA run had
  timestamp `2026-10-10T00:02:29.386535+00:00` and run UUID
  `22a87327-a98f-4295-ac14-e80380fafb23`, with a matching job count. Its
  recorded local path is
  `data/i_work_for_sa/jobs_22a87327-a98f-4295-ac14-e80380fafb23_2026-10-10_10-32-29.json`.
  This is **not** the 14-job release sample. Separate 9 October manual notes
  mention references **860179** and **952110**; these should not be conflated
  with the 11 October sample comparison.
- **Git hygiene (14 October 2026, user-reported):** `.gitignore` excludes
  `data/` and `.venv-wsl/`; `git ls-files -- data/ .venv-wsl/` returned no
  entries after seven runtime JSON files were staged for removal from Git's
  index. Those files remained on disk. Confirm the intended staging and
  curated sample/fixture tracking when preparing the release commit.

### Known limitations

- One site, one category, one results page; manual collection only.
- Source-specific form/table structure; a genuinely empty results table is
  currently treated as an error.
- Size limits are checked after download, **not** enforced by streaming; no
  whole-run hard deadline in this version.
- No retries, scheduling, database, cross-run deduplication, salary numeric
  normalisation, or historical comparisons.
- Live collection and redistribution remain subject to the source-specific
  review and attribution terms; a passing offline test does not guarantee
  continued source availability.

See [KNOWN_LIMITATIONS.md](KNOWN_LIMITATIONS.md) and
[SOURCE_MANIFEST.md](SOURCE_MANIFEST.md). Features explicitly deferred by the
[0.1.0 requirements review](BurrowScout-0.1.0-Requirements-Review-2026-10-11.md)
are not additional blockers for this milestone.

### Final release gate (not claimed complete by this document)

The 11 October live record's original invocation and job-link checks have
now been confirmed. Update any outdated test counts in the README and run
instructions to **32 passed in 0.82 seconds**, verify the curated sample and
fixtures are intentionally tracked, and review the release commit. The user
has confirmed a clean tracked-file index for `data/` and `.venv-wsl/` and the
full passing suite; these facts do **not** themselves prove a release commit
or Git tag exists. Tag **0.1.0** only after the remaining acceptance evidence
is confirmed.
