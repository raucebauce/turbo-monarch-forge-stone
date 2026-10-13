---
name: edge-platform-verify
description: "Verify a venue's API, terms, and availability for a Georgia (US) resident before EDGE builds an adapter or Ross creates a key. Required for every venue; result gates edge-adapter-builder."
type: workflow
lifecycle: active
---
# Platform verify

Use live sources. Cite the URL and date for every claim. Output: GO / NO-GO / DEEP-LINK-ONLY with reasons.

## Check
1. **Residency/ToS**: does the venue serve US residents, and Georgia specifically? Quote the clause.
2. **Official API**: exists, documented, allows programmatic trading (not just read)? Sandbox/testnet?
3. **Key scopes**: can a key be created without withdraw permission? IP allowlist available?
4. **Rate limits & cost**: free tier numbers, paid tier price, per-endpoint limits.
5. **Idempotency**: client order id supported?
6. **Market data**: WebSocket available, or REST polling only?
7. **Legal status changes in the last 12 months** (relevant for prediction markets and sports contracts; search news).
8. **Known API breakages/deprecations** in the last 6 months.

## Decision
- All of 1–3 clear → GO (build adapter).
- Serves Georgia but no trading API → DEEP-LINK-ONLY.
- ToS excludes US/Georgia, or requires misrepresenting residency → NO-GO. No workarounds (Rule 4).

## Output
Venue · decision · evidence table (claim, source URL, date) · env var names if GO · monthly cost · one-line quirk list.

## Output & handoff
- Write the result to `docs/reviews/{date}-verify-{venue}.md`. Include: skill name, inputs (commit/PR/model_version/venue), verdict, evidence table, and `next:` line.
- Append one `changelog` row (actor=<skill>, action, before/after if any, reason=<path to the file>).
- Hands off: GO → edge-adapter-builder; DEEP-LINK-ONLY → edge-cursor-prompt (deep-link adapter); NO-GO → changelog row, stop
- Evidence rows are `claim | file:line or URL | PASS/FAIL/WARN`. No claim without a location.

