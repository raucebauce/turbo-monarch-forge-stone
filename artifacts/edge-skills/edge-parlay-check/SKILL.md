---
name: edge-parlay-check
description: Validate any parlay or correlated-portfolio EDGE proposes — same-book rule, leg correlation, true joint probability vs. book-implied, and surfacing hidden context. Run on every Parlay Lab output before it is shown.
---
# Parlay check

## Hard rules
- All legs on one book, or it is a "correlated portfolio" of singles, never a parlay. Label accordingly.
- No leg with `p_final` missing, stale (>60s for live, >15m pre-game), or from a source with weight 0.
- Max 5 legs by default; more requires Ross to raise the cap in Settings.

## Correlation
- Flag same-game legs (spread + total, QB props + team total, etc.) and compute joint probability with the correlation model, not the product. If no correlation model exists for the pair, refuse the combination and say why.
- Cross-game legs: assume independence only if no shared factor (weather at one venue, same bye-week narrative, same injury). Flag shared factors.

## Numbers shown
- Book-implied parlay probability (de-vigged per leg, then product the book uses).
- EDGE joint probability (correlation-aware).
- Edge % and fractional-Kelly stake; if edge < 0, show it in red and do not suggest a stake.
- Per-leg: p_final, implied p, edge, invalidator, last update age.

## Hidden-context panel (collapsible, never on the card)
Line history, injury timing (hours to kickoff), rest/travel, weather, referee crew, pace, and any "where available" field marked explicitly as unavailable rather than blank.

## Output & handoff
- Parlay record in `picks` as one pick with `category=parlay_<sport>` and legs in `parlay_legs`; Auditor scores both the parlay and each leg.
- Any hard-rule violation → not shown; logged as a rejected parlay with reason.
