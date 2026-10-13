---
name: edge-ux-review
description: Review an EDGE PWA screen or flow against the B5 transition and safety rules — paper/live clarity, stale-data indicators, idempotent buttons, expired deep links, tab-switch state. Use before any screen ships.
---
# UX review

Walk the screen as Ross on iPhone, one thumb, at a game or mid-move. Output: rule | PASS/FAIL | screenshot or file:line | fix.

## Mode clarity
- Live mode changes app chrome color + "LIVE" in tab bar; paper is grey. Visible on every screen, not just Settings.
- Confirm sheet shows platform, mode, size, max loss in large type. Live requires one deliberate confirm; paper logs instantly.
- Mode toggle only in Settings, behind long-press, with exposure summary.

## Data freshness
- Every card shows "updated Xs ago"; amber at 10s, red at 60s (tunable: 5–120s); action buttons disabled on red.
- On `visibilitychange` → resubscribe, "resynced" toast once.

## Buttons & orders
- Button disables on first tap; `idempotency_key` created on sheet open, not on tap.
- Preview re-fetched on sheet open; if price/line moved past tolerance, sheet refuses and re-previews.
- Offline in live mode → refuse with a clear message; offline in paper → queue and reconcile.

## Navigation
- Single WebSocket owned by app shell; tabs subscribe to store slices; switching tabs never reconnects (check network panel).
- `/urgent/{id}` for an expired pick shows the pick + "expired" banner + what happened. Never 404.
- Deep link out to a book → `pending_external` created; on return, ask placed / not placed / changed stake.

## Readability
- Pick card: probability, implied p, edge %, confidence, top-3 reasons, invalidator. History one tap away, not inline.
- Ledger default: by category with ROI, CLV, n, sparkline. Drill-down shows the reason card as it was (immutable).
- Tap targets ≥44pt; contrast ≥4.5:1; numbers in tabular figures.

## Settings safety
- Changing a cap shows affected current exposure and requires confirm.

## Output & handoff
- Write the result to `docs/reviews/{date}-ux-{screen}.md`. Include: skill name, inputs (commit/PR/model_version/venue), verdict, evidence table, and `next:` line.
- Append one `changelog` row (actor=<skill>, action, before/after if any, reason=<path to the file>).
- Hands off: PASS → edge-release mode A; FAIL → edge-cursor-prompt
- Evidence rows are `claim | file:line or URL | PASS/FAIL/WARN`. No claim without a location.
