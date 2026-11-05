---
name: edge-incident
description: Run an EDGE incident — kill switch, contain exposure, reconcile, root-cause, and postmortem. Trigger on reconciliation mismatch, runaway orders, stale data with live mode on, venue outage, key compromise, or any unexpected live loss.
---
# Incident

Order matters. Do not skip to diagnosis.

## 1. Contain (first 60 seconds)
- Flip the global kill switch (phone or `riskgate` admin endpoint). Confirm `state.kill=true` in the gate log.
- Cancel all open live orders via each adapter's `cancel()`; list what could not be cancelled.
- If key compromise suspected: revoke venue keys at the venue first, then in Doppler/1Password.

## 2. Reconcile
- Run the reconciliation job manually; produce venue positions vs. ledger diff per platform.
- Record realized exposure and worst-case open exposure in `docs/incidents/{date}-{slug}.md`.

## 3. Diagnose
- Timeline from `changelog`, gate decisions, adapter logs, Sentry, heartbeats (UTC, then ET).
- Classify: data (stale/wrong feed) · model (bad p) · gate (check missed) · adapter (venue/API) · ops (deploy/infra) · security (key/auth) · human (Ross action).
- Identify the first point a check should have fired and didn't.

## 4. Fix & verify
- Fix via edge-cursor-prompt; review with edge-risk-gate-review; deploy via edge-release mode A.
- Add a regression test named after the incident.

## 5. Resume
- Kill switch stays on until: reconciliation clean, fix deployed, Ross reads the postmortem. All affected strategies return to `paper` regardless of prior status; mode B gate applies again.

## Postmortem (blameless, ≤1 page)
What happened · impact ($, picks) · timeline · root cause · what the gate should have caught · fixes shipped · what changes in a skill or checklist.

## Output & handoff
- Write the result to `docs/incidents/{date}-{slug}.md` (exposure, timeline, postmortem). Include: skill name, inputs (commit/PR/model_version/venue), verdict, evidence table, and `next:` line.
- Append one `changelog` row per action taken (actor=<skill>, action, before/after if any, reason=<path to the file>). Push a 3-line summary to Ross.
- Hands off: fix → edge-cursor-prompt → edge-risk-gate-review → edge-release mode A; a missing check → edge-skill-forge upgrades the skill that should have caught it (PR, Ross approves)
- Evidence rows are `claim | file:line or URL | PASS/FAIL/WARN`. No claim without a location.
