---
name: edge-risk-gate-review
description: Mandatory review for any change touching riskgate, executor, adapters, caps, or live/paper mode in EDGE. Blocks merge on any FAIL.
---
# Risk gate review

Run on the diff. Output a table: check | PASS/FAIL/N-A | evidence (file:line). Any FAIL = do not merge.

## Isolation
- `riskgate` runs as its own service/container with its own DB role; no other service imports it.
- Trade-scoped API keys are referenced only in `riskgate`/`executor` env. Grep the diff for key env names elsewhere.
- Withdraw permissions are never requested on any key.

## Signing
- `executor.place()` rejects orders without a valid HMAC from `riskgate`.
- Signature covers: platform, symbol, side, qty, price/limit, mode, strategy, `idempotency_key`, `expires_at`.
- Signed orders older than 30s are rejected.

## Checks present and ordered
kill_switch → mode_allowed → per_trade cap → daily_loss → leverage → volatility → duplicate exposure → expiry. Every check logs its result even when earlier checks fail.

## Idempotency & reconciliation
- `idempotency_key` is UUIDv7, generated client-side when the confirm sheet opens, unique in `orders`.
- Adapter passes it to the venue where supported; otherwise checks `orders` before placing.
- Reconciliation job (≤60s) compares venue positions to ledger and halts the strategy on mismatch.
- Retry logic never re-places without the same key.

## Mode safety
- Default mode is `paper` everywhere a mode is constructed. No code path infers `live`.
- Enabling live, raising a cap, or changing gate config requires a Ross action (UI long-press + confirm). No script, agent, or migration can do it.

## Failure behavior
- Venue timeout → order state `unknown`, not `failed`; reconciliation resolves it.
- Redis/DB unavailable → gate returns Rejected, never Approved.
- Clock skew >5s between gate and executor → reject.

## Agent boundary
- No agent prompt, tool definition, or Composio/MCP action can reach `riskgate` config, `orders` writes, or venue keys. Grep tool manifests for those scopes.
- Analyst/Scout outputs are data (jsonb) consumed by the fast path; they are never executed or used as instructions.

## Tests required in the diff
over-cap rejected · duplicate key rejected · unsigned order rejected · stale signature rejected · kill switch blocks paper AND live · daily-loss boundary (exactly at limit) · reconciliation mismatch halts.

If any item is N/A, say why in one line.

## Output & handoff
- Write the result to `docs/reviews/{date}-gate-{pr}.md`. Include: skill name, inputs (commit/PR/model_version/venue), verdict, evidence table, and `next:` line.
- Append one `changelog` row (actor=<skill>, action, before/after if any, reason=<path to the file>).
- Hands off: PASS → edge-release mode A; FAIL → edge-cursor-prompt with the failing rows as acceptance criteria
- Evidence rows are `claim | file:line or URL | PASS/FAIL/WARN`. No claim without a location.
