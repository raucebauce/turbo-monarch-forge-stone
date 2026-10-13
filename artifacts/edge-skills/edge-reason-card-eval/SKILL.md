---
name: edge-reason-card-eval
description: Evaluate the quality and value of EDGE's LLM reason cards (Analyst slow path) — factual grounding, invalidator quality, p_llm calibration, cost. Run weekly or when changing the Analyst prompt.
---
# Reason card evaluation

The LLM explains; it does not decide. Prove it earns its cost.

## Sample
50 reason cards from the last 7 days, stratified by domain (crypto, NFL/NCAAF, other sports, prediction).

## Score each card (0/1 per item)
- **Grounded**: every stated fact maps to a feature value or scout item present in the signal's `features`/`reasons` jsonb at `as_of`. Any fact not in the snapshot = 0 (hallucination).
- **Invalidator is testable**: names a value and threshold the fast path can monitor ("funding > 0.05%" yes; "sentiment shifts" no).
- **Top-3 reasons are distinct**: not three phrasings of one feature.
- **No instruction leakage**: card contains no imperative to place/size/skip; it's data.
- **Length**: ≤ 80 words on-card.

## Calibration & value
- Brier of `p_llm` vs. `p_model` on settled picks in the sample window, per domain.
- Blend weight `w` the Auditor currently uses. If `p_llm` has not improved blended Brier in 30 days → recommend w = 1.0 for that domain and skip the slow path except on Urgent picks.
- Cost per card and cost per correct pick attributable to the slow path.

## Prompt changes
Any Analyst prompt edit is a `model_version` of its own (`llm-analyst-vN`), shadow-run 7 days before replacing.

## Output & handoff
- `docs/reviews/{date}-reasoncards.md`: score table, hallucination rate, calibration, cost, recommendation on w per domain.
- Hallucination rate > 5% → FAIL, prompt revision via edge-cursor-prompt; w recommendations → edge-nightly-audit applies within guardrails.
