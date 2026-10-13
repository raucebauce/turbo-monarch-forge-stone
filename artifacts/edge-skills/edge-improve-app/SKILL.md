---
name: edge-improve-app
description: Weekly EDGE application-health loop — pull telemetry, rank defects by user impact, produce one Cursor prompt per fix, open GitHub issues, update docs/IMPROVE_ME.md. Runs Monday 06:00 ET or on demand.
---
# Improve-app loop

Scope: application quality, not model performance (that's edge-nightly-audit).

## Inputs (last 7 days)
Sentry errors grouped by fingerprint · API p50/p95/p99 · WebSocket reconnects per session · push delivery latency p95 (send→receive) · worker restarts and heartbeat gaps · LLM cost per correct pick · Lighthouse CI (PWA, performance, accessibility) · Ross's reported annoyances (from `docs/FEEDBACK.md`).

## Ranking
Score = (users affected: always 1) × frequency × severity (crash 5, wrong data 5, stale data 4, slow 2, cosmetic 1) × money-at-risk (touches orders/ledger ×3).

## Output
1. Top 5 defects with score, evidence, and root-cause hypothesis.
2. One `edge-cursor-prompt`-style prompt per defect, labeled by issue number.
3. GitHub issues tagged `auto-improve`, one per defect, body = the prompt. Do not open duplicates — search first.
4. `docs/IMPROVE_ME.md` updated: weakest area, data that would help most, next build, cost trend.

## Hard limits
Can: open issues, propose prompts, update docs. Cannot: merge, deploy, change gate/caps/mode, rotate keys, touch secrets. If a fix needs any of those, mark it "needs Ross" and stop.

## Output & handoff
- Write the result to `docs/IMPROVE_ME.md + GitHub issues`. Include: skill name, inputs (commit/PR/model_version/venue), verdict, evidence table, and `next:` line.
- Append one `changelog` row (actor=<skill>, action, before/after if any, reason=<path to the file>).
- Hands off: each issue body = edge-cursor-prompt output; Ross approves → Cursor → reviews → edge-release
- Evidence rows are `claim | file:line or URL | PASS/FAIL/WARN`. No claim without a location.
