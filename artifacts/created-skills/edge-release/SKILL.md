---
name: edge-release
description: "Run the EDGE pre-release and go-live checklist for a deploy or for flipping a strategy from paper to live. Produces a signed-off list or a stop."
type: workflow
lifecycle: active
---
# Release / go-live

Two modes. State which.

## A. Code deploy
- CI green (lint, typecheck, pytest, Playwright). Paste run URL.
- Migrations reversible; `down` tested locally.
- `edge-risk-gate-review` run if diff touches gate/executor/adapters — attach result.
- Secrets unchanged or rotated via Doppler/1Password, never in diff.
- Sentry release tagged; heartbeat alerts active.
- Rollback: previous image tag named; one command to revert.
- Post-deploy smoke: Ledger loads, Now tab streams, push test arrives, kill switch toggles from phone.

## B. Strategy paper → live
- Category meets gate: n ≥ 200, ROI > 0, 90% CI lower > −1%, CLV > 0 (sports). Paste the Auditor table.
- Paper fills used the simulator (spread, fees, slippage, latency, rejection). Confirm.
- `edge-leakage-check` passed on this model_version within 30 days.
- Trade-scoped key for this venue created by Ross, no withdraw, IP allowlisted.
- Caps set: per-trade, daily loss, leverage. Starting bankroll on this venue recorded in `bankroll_ledger`.
- Reconciliation job running and green for 24h in paper.
- Kill switch tested from phone in the last 24h.
- Paper-fill simulator validated by `edge-paper-sim-check` within 30 days (simulated fills vs. real sandbox fills within tolerance).
- First 48h live: per-trade cap halved and daily-loss cap halved automatically (config `live_warmup=true`); Auditor restores after 48h clean.
- Ross performs the long-press toggle. Nobody else.

## Output
Checklist with evidence per line. Any unchecked line = STOP, name the blocker, no partial go-live.

## Output & handoff
- Write the result to `docs/releases/{date}-{tag}.md`. Include: skill name, inputs (commit/PR/model_version/venue), verdict, evidence table, and `next:` line.
- Append one `changelog` row (actor=<skill>, action, before/after if any, reason=<path to the file>).
- Hands off: mode A → deploy; mode B → Ross long-press toggle; any STOP → edge-incident if live money is exposed
- Evidence rows are `claim | file:line or URL | PASS/FAIL/WARN`. No claim without a location.

