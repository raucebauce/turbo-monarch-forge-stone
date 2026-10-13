---
name: edge-adapter-builder
description: Build or extend an EDGE venue adapter (Coinbase, Kalshi, Robinhood Crypto, Phemex, Polymarket, or a sportsbook deep-link adapter) against the shared Protocol with sandbox tests.
---
# Adapter builder

Prerequisite: `edge-platform-verify` has cleared this venue. If not, stop.

## Steps
1. **Read the venue docs for**: auth scheme, rate limits, idempotency support (client order id field), sandbox/testnet availability, WebSocket vs REST, order types, precision rules (tick/lot size), error codes.
2. **Implement `packages/shared/adapters/<venue>.py`** satisfying the Protocol exactly: `preview`, `place`, `cancel`, `positions`, `balance`. No extra public methods; venue-specific helpers are private.
3. **Precision**: round qty/price to venue tick/lot before preview; reject if rounding changes notional >0.5%.
4. **Idempotency**: pass `idempotency_key` as the venue client order id. If unsupported, query open orders by a deterministic tag before placing.
5. **Rate limits**: token bucket per endpoint class; back off on 429 with jitter; never retry a `place` without the same key.
6. **Errors**: map venue errors to `AdapterError{kind: auth|rate|reject|network|unknown}`. Network timeout on `place` → return `OrderResult(status="unknown")`.
7. **Deep-link adapters** (no API): `place()` returns a URL + a `pending_external` record; `positions()` returns Ross-confirmed entries only.
8. **Config**: env var names only (`<VENUE>_API_KEY`, `<VENUE>_API_SECRET`, `<VENUE>_SANDBOX=true`). Document them in `docs/ENV.md`.

## Tests (pytest, sandbox or recorded cassettes)
preview→place→cancel round-trip · precision rounding · idempotent double-place returns same order · 429 backoff · timeout → unknown · auth failure → AdapterError(auth) · positions matches a known sandbox state.

## Done report
Venue, endpoints used, rate limits, idempotency method, sandbox availability, env vars, test output, and any venue quirk the next person must know.

## Output & handoff
- Write the result to `docs/reviews/{date}-adapter-{venue}.md`. Include: skill name, inputs (commit/PR/model_version/venue), verdict, evidence table, and `next:` line.
- Append one `changelog` row (actor=<skill>, action, before/after if any, reason=<path to the file>).
- Hands off: → edge-risk-gate-review (mandatory) → edge-release mode A
- Evidence rows are `claim | file:line or URL | PASS/FAIL/WARN`. No claim without a location.
