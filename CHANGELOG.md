# Changelog

All notable changes to this project are documented here. The format follows
[Keep a Changelog](https://keepachangelog.com/en/1.1.0/), and this project uses
[Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

## [1.0.2] - 2026-11-12

### Changed

- The webhook module's docstring uses plain punctuation. The code is the
  same as 1.0.1.

## [1.0.1] - 2026-11-12

### Fixed

- README webhook samples import `os` and read the signature header with
  `.get()`, so a request without the header gets a failed check (401 in the
  Flask sample) instead of a `KeyError`.

## [1.0.0] - 2026-11-12

First release.

- `Kavik` client for single and batch checks, bulk jobs (upload a CSV or XLSX
  file, check status, fetch results as JSON or CSV, wait until done) and
  domain deliverability reports.
- Retries rate-limited and server errors with exponential backoff. A used-up
  daily or monthly allowance is never retried.
- `verify_webhook_signature` and `parse_webhook_event` for signed webhooks.
- Typed errors: `KavikError`, `RateLimitError`, `QuotaExceededError`,
  `DailyLimitError`, `AuthenticationError`, `NotFoundError`,
  `WebhookSignatureError`.
