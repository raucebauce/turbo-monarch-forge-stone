---
name: edge-nightly-audit
description: "Run or interpret the EDGE nightly Auditor pass — settle outcomes, score Brier/ROI/CLV, bootstrap CIs, apply demotions and source weights, write the changelog and the 200-word summary for Ross."
type: workflow
lifecycle: active
---
# Nightly audit (04:10 ET)

## Sequence
1. **Settle**: fetch results/fills/closing lines for picks with `expires_at < now` and no outcome. Sports: postponed games keep `pending` until the rescheduled date + 24h; cancelled → `void`. Crypto/prediction: unresolvable after 48h → `void` and flag the adapter.
   Also settle `pending_external` picks: Ross-confirmed ones score normally; unanswered after 24h → `unknown`, excluded from all stats, counted in a separate `unconfirmed_n` column so the gap is visible.
2. **Score** per model_version × category × source × book, trailing 30d and 90d: n, Brier, log-loss, ROI (net of simulated/actual fees), CLV (sports), hit rate.
3. **Confidence**: 1000-resample bootstrap on ROI; report 90% CI.
4. **Drift**: PSI per feature vs. training distribution; flag >0.2.
5. **Apply rules** (never skip, never soften):
   - Demote model to `paper` if CI lower bound < −2% (n ≥ 50).
   - Source weight: `w = clip(w + 0.1·(sign(roi)·min(|roi|,0.1) + 0.5·(0.25−brier)), 0, 1)` only when n ≥ 30 (tunable: 20–100).
   - Never promote paper→live. Never raise a cap.
6. **Changelog**: one row per change (actor=auditor, before, after, reason).
7. **Summary to Ross** (≤200 words, push): what changed, which category is closest to the live gate (ROI>0, CI lower >−1%, CLV>0, n≥200), top drift flag, cost per correct pick.

## Cost guard
- Sum LLM/API spend per agent for the day vs. `config/agents.yaml` budgets. Any agent >90% of budget → warn; >100% → confirm the orchestrator refused dispatch (log line), else FAIL and open an issue.
- Report cost per correct pick per category; if it exceeds median pick PnL for 14 days, recommend disabling the slow path for that category.

## Interpretation rules
- n < 30 in a category: say "too early", no verdict.
- Positive ROI with negative CLV in sports = likely luck; say so.
- Negative ROI with positive CLV = probably real edge, bad variance; keep in paper, don't retire.
- If LLM `p_llm` blend weight has not improved Brier in 30d, recommend w→1.0 (model only).

## Output
Table of category → n, ROI, CI, CLV, Brier, status. Then the summary. Then the changelog rows written.

## Output & handoff
- Write the result to `changelog rows + docs/audits/{date}.md`. Include: skill name, inputs (commit/PR/model_version/venue), verdict, evidence table, and `next:` line.
- Append one `changelog` row (actor=<skill>, action, before/after if any, reason=<path to the file>).
- Hands off: category meets gate → notify Ross; edge-release mode B is Ross-initiated only
- Evidence rows are `claim | file:line or URL | PASS/FAIL/WARN`. No claim without a location.

