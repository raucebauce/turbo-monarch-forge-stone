---
name: edge-leakage-check
description: "Audit any EDGE backtest, feature, label, or model-evaluation code for lookahead bias and leakage. Use before trusting any accuracy, ROI, or CLV number."
type: workflow
lifecycle: active
---
# Leakage check

A number that survives this check is believable. One that doesn't is noise. Report: finding | severity | fix.

## Features
- Every feature row has `as_of` = the time the value was actually knowable (publish time, not event time).
- Backtest queries use `WHERE as_of <= decision_time`. Grep for any feature join without it.
- Rolling windows are computed with data strictly before the decision timestamp (no `center=True`, no full-series normalization fit before splitting).
- Injury/news features use ingestion timestamp, not the reported event time.
- Odds features use `fetched_at`; "closing line" is only used in outcomes, never as an input.

## Labels
- Crypto: triple-barrier labels evaluated only on bars after the decision bar.
- Sports: outcome joined by game_id AND settled_at > placed_at.
- No label touches a row with `as_of` after the decision.

## Splits
- Sports: walk-forward by week/season. Random k-fold = FAIL.
- Crypto: purged + embargoed k-fold (embargo ≥ label horizon). Plain k-fold = FAIL.
- Scaler/encoder/calibrator fit on train fold only.

## Evaluation
- CLV computed against the line stored at `placed_at` vs. the line at close — both must be rows that existed at those times.
- Paper fills use the simulator (spread, fee, slippage, latency, rejection rate); mid-price fills = FAIL.
- ROI reported with bootstrap CI; a point estimate alone = incomplete.
- Metrics computed per model_version; no mixing of versions in one number.

## Code hygiene
- One `features.py` used by backtest and live. Any notebook-only feature = FAIL.
- Replay test exists: live feature snapshot for a past timestamp == backtest feature row for that timestamp.

## Report format
Finding, file:line, severity (FAIL / WARN), fix. End with "Numbers trustworthy: yes/no" and why.

## Output & handoff
- Write the result to `docs/reviews/{date}-leakage-{model_version}.md`. Include: skill name, inputs (commit/PR/model_version/venue), verdict, evidence table, and `next:` line.
- Append one `changelog` row (actor=<skill>, action, before/after if any, reason=<path to the file>).
- Hands off: trustworthy=yes → numbers may appear in Ledger/summaries; no → model_version.status=candidate, edge-cursor-prompt for fixes
- Evidence rows are `claim | file:line or URL | PASS/FAIL/WARN`. No claim without a location.

