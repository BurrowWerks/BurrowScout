# BurrowScout Source Manifest

## Source

**Source name:** I WORK FOR SA  
**Source identifier:** `i_work_for_sa`  
**Publisher:** I WORK FOR SA / Government of South Australia

**Base URL:**

```text
https://www.iworkfor.sa.gov.au
```

**Search URL:**

```text
https://www.iworkfor.sa.gov.au/jb/page/page.php?pageID=842&windowUID=0
```

## Collection Purpose

BurrowScout collects publicly presented job and wage information for structured
job-market and wage-data research.

Version 0.1.0 is limited to demonstrating reliable retrieval, extraction,
validation, provenance tracking, and local structured output from one source.

## Current Collection Scope

BurrowScout 0.1.0 currently retrieves:

- one configured I WORK FOR SA search
- Accounting and Finance listings
- category identifier `40480`
- one results page per run

BurrowScout does not currently crawl additional categories or automatically
follow pagination.

## Collected Fields

- job title
- reference number
- posting date
- closing date
- agency
- classification
- salary
- location
- job URL

BurrowScout also records:

- source identifier
- source search URL
- UTC observation timestamp
- record count

## Permission / Access Basis

**Review date:** 9 October 2026

The I WORK FOR SA copyright statement says that the Government of South Australia
supports and encourages the dissemination and exchange of public sector
information and endorses the Australian Governments Open Access and Licensing
Framework.

Except for the Piping Shrike emblem, images, trademark-protected material, and
other stated exceptions, the website content is licensed under the Creative
Commons Australia Attribution 3.0 Licence.

Material owned by third parties may require separate permission before reuse.

The I WORK FOR SA disclaimer states that use of information and data from the
site is at the user's own risk and that users are responsible for independently
verifying accuracy, currency, and completeness. The information may change
without notice.

The privacy statement explains that visits are logged for statistical purposes,
including IP address, visit time, pages accessed, documents downloaded, referring
site, and browser type.

### Automated Access

The reviewed Disclaimer, Copyright, and Privacy pages do not expressly grant or
prohibit automated scraping.

BurrowScout therefore does not treat the Creative Commons licence by itself as
explicit permission for unrestricted automated access. Automated collection is
kept deliberately conservative and bounded by the request policy documented
below.

Before materially increasing request volume, adding crawling, or using the
source in a broader public/commercial deployment, the source terms and any
applicable robots.txt directives should be reviewed again.

## Reviewed Source Policies

- Disclaimer:
  `https://www.iworkfor.sa.gov.au/iworkforsa/disclaimer.php`
- Copyright:
  `https://www.iworkfor.sa.gov.au/iworkforsa/copyright.php`
- Privacy:
  `https://www.iworkfor.sa.gov.au/iworkforsa/privacy.php`

## Attribution

Data collected from this adapter originates from I WORK FOR SA / Government of
South Australia.

BurrowScout preserves the source job URL where available so individual records
can be traced back to their source listing.

Reuse of licensed website content should include attribution consistent with the
Creative Commons Australia Attribution 3.0 Licence. Third-party material and
excluded visual/trademark material should not be assumed to be covered by that
licence.

## Request Policy

### User-Agent

```text
BurrowScout/0.1.0 (Python; wage-data research)
```

BurrowScout identifies itself truthfully rather than impersonating a browser.

### Timeout

Connection timeout:

```text
5 seconds
```

Read timeout:

```text
30 seconds
```

### Maximum Response Size

```text
5 MiB
5,242,880 bytes
```

The current 0.1.0 implementation checks response size after the response has
been downloaded.

A streamed hard-download limit is deferred to later reliability work.

### Page Limit

```text
1 results page per run
```

BurrowScout 0.1.0 does not implement pagination.

## Request Sequence

The current adapter performs:

1. GET the stable I WORK FOR SA search endpoint.
2. Validate the response.
3. Extract the dynamic `jobboard_token`.
4. POST the configured search using the same HTTP session.
5. Validate the returned result page.
6. Pass the returned HTML to the parser.

## Structural Validation

BurrowScout expects the result table:

```text
#brs_report_table_16
```

Job rows are selected from:

```text
tr.evenrow
tr.oddrow
```

Each supported result row is expected to contain exactly eight table cells.

Unexpected structure causes the run to fail rather than silently producing
potentially incorrect data.

## Storage

Collected data is written locally as UTF-8 JSON.

Raw HTML retention is not part of the normal 0.1.0 collection process.

## Review Triggers

This manifest should be reviewed whenever:

- source terms or licensing change
- robots.txt directives change
- the website structure changes substantially
- new categories are added
- pagination or crawling is implemented
- collection frequency increases
- new data fields are collected
- use expands materially beyond the current research scope
