---
name: edge-source-onboard
description: "Onboard a new data or social source into EDGE (sources table, ingest worker, cost budget, starting weight 0, accuracy tracking). Use before any new feed, RSS, subreddit, Discord server, capper, or news API is consumed."
type: workflow
lifecycle: active
---
# Source onboarding

A source is untrusted until the Auditor says otherwise. Onboarding makes it measurable; it does not make it trusted.

## Before ingesting
- Kind: api | rss | social | human. Official access path (Rule 4). Cost/day and rate limit.
- What it emits: a feature (goes to `features.py` via edge-feature-spec) or a claim/pick (scored as a source). Pick one. A capper's picks are claims; a weather feed is a feature.
- Timestamp of knowability: which field becomes `as_of`. If none exists, use ingest time and say so.
- Dedup key for items; retention window.

## Implement
- Row in `sources` with weight 0.0, `cost_per_day`, `enabled=true`.
- Ingest worker under the matching `ingest-*` service; writes raw items with `source_id`, `as_of`, `fetched_at`, `content_hash`; publishes to its Redis Stream.
- Claims parsed into `source_claims(source_id, market, side, line, odds, stated_at, resolved_pick_id)` so the Auditor can score them like picks without ever placing them.
- Daily spend cap in `config/sources.yaml`; worker stops at cap and logs.

## Tests
reconnect after drop · dedup on replay · `as_of` never after `fetched_at` · cap stops ingestion · malformed item does not crash the worker.

## Output & handoff
- Write to `docs/sources/{name}.md`: access path, cost, kind, as_of field, dedup key, starting weight 0.
- Hands off: feature-type → edge-feature-spec; claim-type → edge-nightly-audit scores it after n ≥ 30; weight 0 for 30 days with n < 30 → auto-disable and changelog it.

