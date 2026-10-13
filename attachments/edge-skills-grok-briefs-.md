# EDGE Skills — Grok Creation Briefs (16, individual)

**Grok, read this first.** The SKILL.md body for every skill already exists in `edge-skills-v2.1.zip` — use it verbatim as the skill body. Do not rewrite it. This file supplies what your `init_skill.py` / skill-creator pipeline needs on top: purpose, triggers, negative triggers, inputs/outputs, and evals. Create each skill **individually**, in the order listed, and validate each before starting the next. For every skill:

1. `init_skill.py <name>` → paste the SKILL.md from the zip.
2. Fill `triggers.json` from the "Should trigger" / "Should NOT trigger" lists below.
3. Add `evals/` from the "Evals" list — each eval is a prompt + the check that proves the skill ran correctly.
4. `CHANGELOG.md`: `v2.1 — initial import from edge-skills-v2.1.zip`.
5. Validate. Report: skill name, files created, eval results. Then the next one.

Common to all 16: **Output** is a file under `docs/` (path stated in each SKILL.md's Output & handoff block) plus one `changelog` row; **evidence format** is `claim | file:line or URL | PASS/FAIL/WARN`. An eval passes only if the output file exists, has the evidence table, and has a `next:` line.

The sentence you asked me to finish — "This skill should:" — is answered under **Purpose** for each skill below.

---

## 1. edge-platform-verify
**Purpose.** This skill should verify a venue's official API, terms of service, and availability for a Georgia (US) resident, and return GO / NO-GO / DEEP-LINK-ONLY with dated URL evidence, before any key is created or adapter written.
**Should trigger:** "Can we build the Phemex adapter?" · "Verify Kalshi for Georgia before I make a key" · "Is Polymarket usable from the US right now?"
**Should NOT trigger:** "Write the Coinbase WebSocket ingest worker" (that's edge-cursor-prompt; verify already done).
**Inputs:** venue name; live web access. **Output:** `docs/reviews/{date}-verify-{venue}.md`.
**Evals:** (a) Phemex → output contains a quoted ToS clause with URL and date, decision is NO-GO or DEEP-LINK-ONLY, no workaround suggested. (b) Coinbase → GO, lists key scopes without withdraw, names env vars. (c) Any venue → every claim row has a URL; a row without one fails the eval.

## 2. edge-source-onboard
**Purpose.** This skill should register a new data/social source with weight 0, an ingest worker, a cost cap, an `as_of` field, and a dedup key, so the Auditor can measure it before anyone trusts it.
**Should trigger:** "Add r/CFB as a source" · "Hook up this capper's Substack RSS" · "Start ingesting the Sleeper trending-adds endpoint"
**Should NOT trigger:** "Which sources have the best CLV this month?" (edge-nightly-audit).
**Inputs:** source identity, access path, kind (api/rss/social/human). **Output:** `docs/sources/{name}.md` + `sources` row.
**Evals:** (a) Capper RSS → classified as claim-type, `source_claims` parsing specified, weight 0. (b) Weather API → classified as feature-type, hands off to edge-feature-spec. (c) Any → `as_of` field named; if none exists, output says "ingest time" explicitly.

## 3. edge-cursor-prompt
**Purpose.** This skill should produce one self-contained Cursor prompt for a single build step with exact files, pasted interfaces, invariants, named tests, acceptance criteria, out-of-scope list, done signal, a budget line, and the receipt contract with routing flags.
**Should trigger:** "Write the Cursor prompt for step 5, the risk gate" · "I need Cursor to build the Urgent tab" · "Turn this GitHub issue into a Cursor task"
**Should NOT trigger:** "Review the risk gate diff Cursor just produced" (edge-risk-gate-review).
**Inputs:** step number or task description; relevant spec sections. **Output:** `docs/prompts/{nn}-{slug}.md`.
**Evals:** (a) Step 5 → prompt contains the Adapter Protocol verbatim, names ≥1 failure-path test, ends with the receipt contract including `touched_gate`. (b) A task needing 12 files → skill splits it into two prompts. (c) Any → no phrase "add appropriate tests"; no secret values, env var names only.

## 4. edge-adapter-builder
**Purpose.** This skill should build a venue adapter that satisfies the shared Protocol exactly, with precision rounding, idempotency, rate-limit backoff, error mapping, sandbox tests, and a done report of venue quirks.
**Should trigger:** "Build the Kalshi adapter" · "Implement Coinbase preview/place/cancel against sandbox" · "Make a deep-link adapter for DraftKings"
**Should NOT trigger:** "Is Kalshi legal in Georgia?" (edge-platform-verify must run first; this skill refuses if no GO file exists).
**Inputs:** venue, GO file from edge-platform-verify, venue docs. **Output:** `docs/reviews/{date}-adapter-{venue}.md` + code.
**Evals:** (a) No GO file for the venue → skill stops and says so. (b) Coinbase → tests listed include idempotent double-place and timeout→unknown. (c) Deep-link venue → `place()` returns URL + `pending_external`, never claims a fill.

## 5. edge-feature-spec
**Purpose.** This skill should add one model input to the single `features.py` with a stated hypothesis, `as_of` discipline, None-on-missing, registry entry, parity/staleness/no-future tests, and a PSI baseline.
**Should trigger:** "Add referee crew tendencies as a feature" · "I want funding-rate delta in the crypto model" · "New feature: hours between injury report and kickoff"
**Should NOT trigger:** "Why did the model's Brier get worse this week?" (edge-nightly-audit).
**Inputs:** feature idea, source table. **Output:** `docs/features/{name}.md` + code + tests.
**Evals:** (a) Feature with no stated hypothesis → skill refuses. (b) Any → returns None on missing, never 0. (c) Any → no-future test present (row with `as_of > decision_time` leaves value unchanged).

## 6. edge-risk-gate-review
**Purpose.** This skill should review any diff touching riskgate/executor/adapters/mode/agent tool scopes against isolation, signing, check order, idempotency, reconciliation, mode safety, failure behavior, agent boundary, and required tests; any FAIL blocks merge.
**Should trigger:** "Review this riskgate PR" · "Cursor finished the executor, check it" · "Did the new Analyst tool manifest touch anything it shouldn't?"
**Should NOT trigger:** "Review the Ledger page layout" (edge-ux-review).
**Inputs:** diff or PR. **Output:** `docs/reviews/{date}-gate-{pr}.md`.
**Evals:** (a) Diff that lets executor accept unsigned orders → FAIL on Signing, verdict do-not-merge. (b) Diff with a script that sets `live_enabled=true` → FAIL on Mode safety. (c) Clean diff → every row PASS or N/A-with-reason, no empty cells.

## 7. edge-leakage-check
**Purpose.** This skill should audit features, labels, splits, evaluation, and code hygiene for lookahead bias and leakage, and end with "Numbers trustworthy: yes/no" and why.
**Should trigger:** "Audit the NFL backtest before I believe the ROI" · "Is this crypto model leaking?" · "Check model_version nfl-v3 for lookahead"
**Should NOT trigger:** "Add a new feature for pace" (edge-feature-spec, which then calls this).
**Inputs:** backtest/model code, model_version. **Output:** `docs/reviews/{date}-leakage-{model_version}.md`.
**Evals:** (a) Random k-fold on sports → FAIL. (b) Feature join without `as_of <=` → FAIL with file:line. (c) Mid-price paper fills → FAIL; verdict "trustworthy: no".

## 8. edge-paper-sim-check
**Purpose.** This skill should compare simulated fills to real sandbox/small-live fills (≥50 pairs per venue), report price/fee/latency/rejection error, flag optimistic bias as FAIL, and gate any paper→live flip.
**Should trigger:** "Validate the paper simulator for Coinbase" · "Before I go live on NFL spreads, is paper honest?" · "We changed the slippage function — recheck"
**Should NOT trigger:** "Flip NFL spreads to live" (edge-release mode B, which requires this skill's PASS first).
**Inputs:** venue, matched fill pairs. **Output:** `docs/reviews/{date}-papersim-{venue}.md`.
**Evals:** (a) 30 pairs → "insufficient sample", no verdict. (b) Sim 2 bps better than real → FAIL (optimistic bias). (c) Within tolerance → PASS with the error table.

## 9. edge-parlay-check
**Purpose.** This skill should validate every Parlay Lab output: same-book rule, no stale/weight-0 legs, correlation-aware joint probability, refuse pairs with no correlation model, and surface hidden context in a collapsible panel.
**Should trigger:** "Check this 4-leg NFL parlay" · "Is this same-game parlay correlated?" · "Build me a cross-sport parlay for Saturday" (runs after the builder, before display)
**Should NOT trigger:** "What's the ROI on parlays this month?" (edge-nightly-audit).
**Inputs:** proposed legs with book, odds, p_final, update age. **Output:** parlay record in `picks` or a logged rejection.
**Evals:** (a) Legs from two books → labeled "correlated portfolio", not parlay. (b) Spread + total same game, no correlation model → refused with reason. (c) Edge < 0 → shown red, no stake suggested.

## 10. edge-reason-card-eval
**Purpose.** This skill should score 50 stratified LLM reason cards for grounding, testable invalidators, distinct reasons, no instruction leakage, and length; compute p_llm calibration and cost; recommend blend weight per domain.
**Should trigger:** "Are the Analyst reason cards actually accurate?" · "Weekly reason card eval" · "I changed the Analyst prompt — evaluate it"
**Should NOT trigger:** "Write the Analyst prompt" (edge-cursor-prompt).
**Inputs:** last 7 days of reason cards + signal snapshots + settled outcomes. **Output:** `docs/reviews/{date}-reasoncards.md`.
**Evals:** (a) Card citing a fact absent from the `features` snapshot → scored 0 on Grounded. (b) Hallucination rate 8% → FAIL, prompt revision routed. (c) p_llm no Brier improvement in 30d → recommends w=1.0.

## 11. edge-ux-review
**Purpose.** This skill should walk a PWA screen as a one-thumb iPhone user and check mode clarity, freshness indicators, idempotent buttons, navigation/deep-link behavior, readability, and settings safety.
**Should trigger:** "Review the Urgent tab before it ships" · "UX check on the confirm sheet" · "Does the Ledger pass the B5 rules?"
**Should NOT trigger:** "Review the riskgate service" (edge-risk-gate-review).
**Inputs:** screen/flow, build or screenshots. **Output:** `docs/reviews/{date}-ux-{screen}.md`.
**Evals:** (a) Live mode with no chrome color change → FAIL. (b) `/urgent/{id}` returns 404 for an expired pick → FAIL. (c) Button stays enabled after first tap → FAIL.

## 12. edge-nightly-audit
**Purpose.** This skill should settle outcomes, score Brier/ROI/CLV with bootstrap CIs per model/source/category/book, check drift and agent cost, apply demotions and weight updates within guardrails, write changelog rows, and push a ≤200-word summary.
**Should trigger:** "Run the nightly audit" · "Interpret last night's Auditor output" · "Which category is closest to the live gate?"
**Should NOT trigger:** "Promote the NFL model to live" (Ross-only via edge-release B).
**Inputs:** picks, outcomes, model_versions, config/agents.yaml. **Output:** changelog rows + `docs/audits/{date}.md`.
**Evals:** (a) Category with n=20 → "too early", no verdict. (b) ROI +4% but CLV −1% in sports → flagged as likely luck. (c) Never emits a paper→live promotion; eval fails if any changelog row does.

## 13. edge-improve-app
**Purpose.** This skill should pull a week of telemetry, rank defects by impact × frequency × severity × money-at-risk, produce one Cursor prompt per top-5 defect, open deduped GitHub issues, and update IMPROVE_ME.md — without merging or deploying.
**Should trigger:** "Monday app-health loop" · "What's broken in the app this week?" · "Turn the Sentry errors into Cursor tasks"
**Should NOT trigger:** "Which model should be retrained?" (edge-nightly-audit / weekly retrain).
**Inputs:** Sentry, latency, push latency, worker restarts, Lighthouse, FEEDBACK.md. **Output:** issues + `docs/IMPROVE_ME.md`.
**Evals:** (a) Defect touching `orders` → score ×3 and ranked above cosmetic. (b) Existing open issue for same fingerprint → no duplicate opened. (c) Fix needing a cap change → marked "needs Ross", not proposed as a prompt.

## 14. edge-release
**Purpose.** This skill should run the deploy checklist (mode A) or the paper→live checklist (mode B) with evidence per line; any unchecked line is a STOP with the blocker named.
**Should trigger:** "Release step 6 to prod" · "Go-live checklist for crypto spot" · "Can NFL totals go live yet?"
**Should NOT trigger:** "Run the tests" (that's inside Cursor's receipt, not a release).
**Inputs:** mode, CI run, Auditor table, review files. **Output:** `docs/releases/{date}-{tag}.md`.
**Evals:** (a) Mode B with n=150 → STOP, blocker "n < 200". (b) Mode B with no edge-paper-sim-check in 30d → STOP. (c) Mode A with gate diff and no risk-gate-review file → STOP.

## 15. edge-incident
**Purpose.** This skill should contain first (kill switch, cancel all, revoke keys if compromise), then reconcile, diagnose with a UTC timeline, fix through the normal chain, return all affected strategies to paper, and write a blameless one-page postmortem.
**Should trigger:** "Reconciliation mismatch on Coinbase" · "Orders are firing that I didn't approve" · "Feed went stale with live mode on"
**Should NOT trigger:** "A unit test is failing in CI" (edge-cursor-prompt).
**Inputs:** alert or Ross report; logs, changelog, gate decisions. **Output:** `docs/incidents/{date}-{slug}.md`.
**Evals:** (a) Any trigger → first action in the output is kill switch confirmation, before any diagnosis. (b) After fix → affected strategies' status is `paper` regardless of prior. (c) Postmortem names what the gate should have caught.

## 16. edge-skill-forge
**Purpose.** This skill should detect a recurring procedure, gap, or incident lesson; draft a new skill or an upgrade in house format; lint it against guardrails; shadow-run 7 days; and propose it as a PR that only Ross can merge.
**Should trigger:** "Make this a skill" · "We've done this three times by hand this week" · "The incident showed risk-gate-review missed a check — fix the skill"
**Should NOT trigger:** "Raise the daily loss cap" (never a skill-forge action; Ross-only in Settings).
**Inputs:** changelog, incidents, reviews, IMPROVE_ME.md, current skill set. **Output:** `docs/skills/{date}-{name}.md` + PR.
**Evals:** (a) Draft that removes an Output & handoff block → rejected at lint. (b) Draft granting an agent a new tool scope → rejected at lint. (c) Approved skill → changelog row `skill_installed` with PR link; eval fails if the skill loaded without one.

---

**Order to create:** 1 → 3 → 6 → 7 → 14 → 15 first (they gate everything), then 2, 4, 5, 8, 9, 10, 11, 12, 13, 16.
