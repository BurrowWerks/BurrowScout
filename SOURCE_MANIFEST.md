**# BurrowScout Source Manifest**

**## Source**

****Source name:**** I WORK FOR SA

****Source identifier:**** `i_work_for_sa`

****Publisher:**** I WORK FOR SA / Government of South Australia

****Base URL:****

```text

https://www.iworkfor.sa.gov.au

```

****Search URL:****

```text

https://www.iworkfor.sa.gov.au/jb/page/page.php?pageID=842&windowUID=0

```

**## Collection Purpose**

BurrowScout collects publicly presented job and wage information for structured

job-market and wage-data research.

Version 0.1.0 is limited to demonstrating reliable retrieval, extraction,

validation, provenance tracking, and local structured output from one source.

**## Current Collection Scope**

BurrowScout 0.1.0 currently retrieves:

- one configured I WORK FOR SA search

- Accounting and Finance listings

- category identifier `40480`

- one results page per run

BurrowScout does not currently crawl additional categories or automatically

follow pagination.

**## Collected Fields**

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

**### Salary Field Policy**

For BurrowScout 0.1.0, `job_salary` stores the non-empty salary text presented

by the source.

The value is preserved as source text and is not interpreted as an exact

numeric wage.

Valid values may therefore include:

- broad ranges such as `$70k - $89k`

- multiple ranges such as `$90k - $109k, $110k - $149k`

- undisclosed-pay wording such as `Negotiable`

Listings with non-numeric salary wording are retained as contextual job records.

BurrowScout 0.1.0 does not convert salary text into numeric minimum/maximum

values or infer or invent remuneration that the source does not provide.

Values such as `Negotiable` remain valid contextual job data. Future numeric

wage datasets or exports will need to distinguish or exclude undisclosed-pay

records rather than treating them as numerical wage observations.

**## Permission / Access Basis**

****Review date:**** 9 October 2026

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

**### Source Review Outcome**

****Reviewer:**** Richard Martin

****Original review date:**** 9 October 2026

****Robots review completed:**** 11 October 2026

****Project review outcome:**** Approved for BurrowScout 0.1.0's current bounded

research use.

This approval is limited to:

- the I WORK FOR SA source

- the Accounting and Finance category (`40480`)

- one results page per run

- manual execution only

- the documented request interval, timeout, response-size and redirect controls

- collection of the fields documented in this manifest

This is an internal BurrowScout source-review decision. It is not a claim that

the publisher has expressly authorised automated scraping, and it is not a legal

determination.

The reviewed Disclaimer, Copyright and Privacy pages do not expressly grant or

prohibit automated collection. The website's content licence is treated

separately from permission to access the site automatically.

**### Collection Frequency**

BurrowScout 0.1.0 is manual-run only. It does not contain scheduling or

continuous collection functionality.

For the 0.1.0 source policy, repeated manual runs should not be performed more

frequently than once per hour unless the source is reviewed again and a

different limit is documented.

Each request within a run is also subject to BurrowScout's configured minimum

request interval.

**### Robots.txt Review**

****Review date:**** 11 October 2026

The published `robots.txt` file was reviewed and returned:

```text

User-agent: *

Disallow:

```

No paths are disallowed by the current `robots.txt`.

This result is recorded separately from the legal and policy basis for

collection. An empty `Disallow` directive is not treated as a general grant of

permission for unrestricted automated access.

The `robots.txt` file must be reviewed again before introducing automated

scheduling, crawling, pagination, materially higher request volume, or

additional collection paths.

**### Shared Output and Attribution**

Any publicly shared BurrowScout output derived from I WORK FOR SA should identify

I WORK FOR SA / Government of South Australia as the source and preserve source

URLs where available.

Reuse of website content should comply with the applicable Creative Commons

Australia Attribution 3.0 Licence and its attribution requirements. Material

identified as third-party content, trademark-protected material, images, or

other excluded material must not be assumed to be covered by that licence.

BurrowScout's own source code remains governed separately by the project's MIT

licence.

**### Automated Access**

The reviewed Disclaimer, Copyright, and Privacy pages do not expressly grant or

prohibit automated scraping.

BurrowScout therefore does not treat the Creative Commons licence by itself as

explicit permission for unrestricted automated access. Automated collection is

kept deliberately conservative and bounded by the request policy documented

below.

Before materially increasing request volume, adding crawling, or using the

source in a broader public/commercial deployment, the source terms and any

applicable robots.txt directives should be reviewed again.

**## Reviewed Source Policies**

- Disclaimer:

  `https://www.iworkfor.sa.gov.au/iworkforsa/disclaimer.php`

- Copyright:

  `https://www.iworkfor.sa.gov.au/iworkforsa/copyright.php`

- Privacy:

  `https://www.iworkfor.sa.gov.au/iworkforsa/privacy.php`

**## Request Policy**

**### User-Agent**

```text

BurrowScout/0.1.0 (Python; wage-data research)

```

BurrowScout identifies itself truthfully rather than impersonating a browser.

**### Timeout**

Connection timeout:

```text

5 seconds

```

Read timeout:

```text

30 seconds

```

**### Maximum Response Size**

```text

5 MiB

5,242,880 bytes

```

The current 0.1.0 implementation checks response size after the response has

been downloaded.

BurrowScout 0.1.0 intentionally uses a post-download response-size check rather

than a streamed hard-download limit.

A true streamed download budget is deferred to BurrowScout 0.2.0 reliability

work. Version 0.1.0 is limited to manual, single-category, single-page runs and

uses connection/read timeouts, request spacing, bounded redirects, and the

post-download 5 MiB validation as its current request safeguards.

**### Overall Runtime Limit**

BurrowScout 0.1.0 does not enforce a hard whole-run deadline.

Individual network operations are bounded by the configured connection and read

timeouts, but these are not equivalent to a maximum total run duration.

A hard whole-run runtime budget is deferred to BurrowScout 0.2.0 reliability work.

**### Page Limit**

```text

1 results page per run

```

BurrowScout 0.1.0 does not implement pagination.

**### Redirect Boundary**

BurrowScout 0.1.0 follows only redirects required by the documented

I WORK FOR SA search workflow.

An approved redirect destination must satisfy all of the following:

- use the `https` scheme

- use the hostname `www.iworkfor.sa.gov.au`

- use the standard HTTPS port, either implicitly or explicitly as port `443`

- have a normalised path beginning with `/jb/page/`

- contain no embedded username or password credentials

Redirect URLs are resolved and normalised before the destination scope is

validated. This prevents path components such as `..` from escaping the

approved `/jb/page/` boundary after URL normalisation.

Query strings are permitted for destinations that otherwise satisfy the

approved scheme, host, port and path boundary. Query parameters do not expand

the approved URL scope.

The 0.1.0 adapter does not implement a general redirect-following loop. Its

fixed workflow follows at most two approved redirect destinations and performs

at most four requests:

1. GET the configured stable search endpoint

2. GET the validated redirected search page

3. POST the configured search to the stable endpoint

4. GET the validated redirected results page

A redirect that fails validation is rejected before its destination is

requested. An unexpected additional redirect is not followed.

**## Request Sequence**

The current adapter performs:

GET stable endpoint

→ receive 302

→ normalise and validate approved redirect

→ GET redirected search page

→ validate HTML

→ extract jobboard_token

→ POST configured search

→ receive 302

→ normalise and validate approved redirect

→ GET redirected results page

→ validate HTML

→ parse

**## Structural Validation**

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

**## Storage**

Collected data is written locally as UTF-8 JSON.

Raw HTML retention is not part of the normal 0.1.0 collection process.

**## Review Triggers**

This manifest should be reviewed whenever:

- source terms or licensing change

- robots.txt directives change

- the website structure changes substantially

- new categories are added

- pagination or crawling is implemented

- collection frequency increases

- new data fields are collected

- use expands materially beyond the current research scope

## URL Resolution Contract — 0.1.0

Manual live verification on 11 October 2026 confirmed that I WORK FOR SA returned root-relative `/jb/page/...` values for both HTTP `Location` redirect headers and job listing `href` attributes. BurrowScout 0.1.0 therefore supports the observed root-relative and absolute URL forms. Path-relative forms such as `page.php?...` or `?pageID=...` were not observed and are outside the verified 0.1.0 source contract.
