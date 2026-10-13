---
name: edge-feature-spec
description: "Add a new feature to EDGE's single features.py module with as_of discipline, drift baseline, and a live/backtest parity test. Use for any new model input (crypto, sports, social, news)."
type: workflow
lifecycle: active
---
# Feature spec

## Before writing code, answer
- Source table and the column that gives `as_of` (publish/ingest time).
- Expected update frequency and staleness tolerance.
- Hypothesis: why this should predict the target. One sentence. If you can't, don't add it.
- Leakage risk: could this value ever be revised after the fact? If yes, store first-seen value.

## Implementation
- Function in `packages/shared/features.py`: `def f_<name>(symbol_or_game, decision_time, conn) -> float | None`.
- Uses only rows with `as_of <= decision_time`.
- Returns `None` when unavailable; never 0 or a fill value (the model handles missing explicitly).
- Register in `FEATURE_REGISTRY` with: name, domain, dtype, hypothesis, source_id, added_on.

## Tests
- Parity: value at a past timestamp via live path == via backtest path.
- Staleness: returns None past tolerance.
- No-future: inject a row with `as_of > decision_time`; value unchanged.

## After merge
- Compute PSI baseline on the training window; store in `model_versions.metrics.psi_baseline`.
- Feature enters the next weekly retrain as candidate; the Auditor reports its importance and whether Brier/CLV moved.

## Output & handoff
- Write the result to `docs/features/{name}.md`. Include: skill name, inputs (commit/PR/model_version/venue), verdict, evidence table, and `next:` line.
- Append one `changelog` row (actor=<skill>, action, before/after if any, reason=<path to the file>).
- Hands off: → edge-leakage-check (mandatory) → weekly retrain registers candidate → edge-nightly-audit reports importance
- Evidence rows are `claim | file:line or URL | PASS/FAIL/WARN`. No claim without a location.

