# BurrowScout 0.1.0 Known Limitations

BurrowScout 0.1.0 is intentionally limited to proving the core scraping and
structured-output workflow.

## Single Source

Only I WORK FOR SA is currently supported.

## Single Search Category

The current scraper submits only the Accounting and Finance search using
category `40480`.

## Salary Precision

BurrowScout 0.1.0 records the salary representation presented in the
I WORK FOR SA search-results table.

This may be a broad salary band such as `$70k - $89k` rather than the
more precise remuneration range shown on the individual job-detail page.

Version 0.1.0 does not follow each listing to retrieve detailed remuneration.

## No Pagination

Only the first returned results page is processed.

## Zero Results Treated as an Error

The parser currently treats an empty result table as a failure and does not yet
distinguish reliably between a legitimate zero-result search and a broken page.

## Response Limit Is Not a Hard Download Limit

Responses larger than 5 MiB are rejected after they have been received.

Because requests are not currently streamed, the complete response is downloaded
before the size validation occurs.

## No Automatic Retries

Transient HTTP failures are not automatically retried.

## Website-Specific HTML Structure

The parser depends on I WORK FOR SA's current table ID, row classes, column
count, form fields, and token workflow.

## Form Workflow Dependency

The source currently requires an initial GET, extraction of a dynamic token,
and a POST using the same HTTP session.

## No Database

Version 0.1.0 writes local JSON only. There is no SQLite, DuckDB, historical
database, or cross-run duplicate tracking.

## No Scheduling

Runs must currently be started manually.

## No Historical Comparison

BurrowScout does not currently identify newly posted jobs, removed jobs, salary
changes, or closing-date changes between runs.

## No General Configuration System

Source IDs, URLs, category values, and request behaviour are currently defined
directly in the application.

## Source Permission Must Remain Reviewed

Collection should only be performed against sources whose use has been reviewed
and approved for the project. Changes to a source's terms or restrictions may
require collection to stop until review is completed.
