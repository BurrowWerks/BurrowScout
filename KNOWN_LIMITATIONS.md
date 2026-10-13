# BurrowScout 0.1.0 Known Limitations

BurrowScout 0.1.0 is intentionally limited to proving the core scraping and
structured-output workflow.

## Single Source

Only I WORK FOR SA is currently supported.

## Single Search Category

The current scraper submits only the Accounting and Finance search using
category `40480`.

## Salary Precision

Salary values are preserved as presented by the search-results source.
BurrowScout 0.1.0 does not convert salary text into numeric minimum/maximum
values or infer missing remuneration.

Values such as `Negotiable` remain valid contextual job data. Multiple salary
bands are also preserved as source text.

Future numeric wage datasets or exports will need to distinguish or exclude
undisclosed-pay records rather than treating them as numerical wage observations.


## No Pagination

Only the first returned results page is processed.

## Zero Results Treated as an Error

The parser currently treats an empty result table as a failure and does not yet
distinguish reliably between a legitimate zero-result search and a broken page.

## Response Limit Is Not a Hard Download Limit

Responses larger than 5 MiB are rejected after they have been received.

Because requests are not currently streamed, the complete response is downloaded
before the size validation occurs.

BurrowScout 0.1.0 intentionally uses a post-download response-size check rather
than a streamed hard-download limit.

A true streamed download budget is deferred to BurrowScout 0.2.0 reliability
work. Version 0.1.0 is limited to manual, single-category, single-page runs and
uses connection/read timeouts, request spacing, bounded redirects, and the
post-download 5 MiB validation as its current request safeguards.

## No Hard Overall Runtime Limit

BurrowScout 0.1.0 does not enforce a hard whole-run deadline.

Individual network operations are bounded by the configured connection and read
timeouts, but these are not equivalent to a maximum total run duration.

A hard whole-run runtime budget is deferred to BurrowScout 0.2.0 reliability
work.

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
