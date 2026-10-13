---
name: edge-paper-sim-check
description: Validate EDGE's paper-fill simulator against real sandbox or small live fills so paper ROI is believable. Required before any paper→live flip and after any simulator change.
---
# Paper simulator check

Paper results are only as honest as the fill model. Measure it.

## Method
1. Collect ≥50 matched pairs per venue: simulator fill vs. real fill (sandbox, or live orders ≤ $10 notional in a dedicated test strategy) for the same intent at the same timestamp.
2. Compare: fill price error (bps), fee error, latency error, and for sports the rejection rate (simulated 10% vs. observed).
3. Tolerance: median |price error| ≤ 3 bps crypto spot, ≤ 8 bps perps; fee error 0; sports rejection rate within ±5 points of observed.
4. If outside tolerance: recalibrate the slippage function `f(order_size / top_of_book_depth)` and latency constants; re-run.
5. Report simulator bias direction. Optimistic bias (sim better than real) is a FAIL regardless of magnitude.

## Also verify
- Paper uses the order book at `as_of` ≤ decision time, not a later snapshot.
- Partial fills modeled when size > top-of-book depth.
- Funding/borrow costs applied to perps held across funding timestamps.

## Output & handoff
- Write to `docs/reviews/{date}-papersim-{venue}.md` with the error table and verdict.
- PASS → edge-release mode B may proceed; FAIL → `model_versions` for that venue stay `candidate`, edge-cursor-prompt for simulator fixes.
