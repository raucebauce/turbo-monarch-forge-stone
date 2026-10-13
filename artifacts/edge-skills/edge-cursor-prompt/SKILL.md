---
name: edge-cursor-prompt
description: Write one self-contained Cursor build prompt for a single EDGE step (from the B3 sequence or a new task). Use whenever code needs to be written.
---
# Cursor prompt for one EDGE step

Produce ONE prompt Ross pastes into Cursor. It must stand alone — Cursor has no memory of the spec.

## Always include, in this order
1. **Context block** (≤10 lines): repo layout (`apps/web`, `apps/api`, `apps/workers`, `packages/shared`, `infra/`), stack (Python 3.12 FastAPI + asyncio, Next.js + Tailwind + Zustand, Timescale, Redis Streams), and the 5 operating rules from Part A compressed to one line each.
2. **Goal**: one sentence. What exists when this step is done.
3. **Files to create/modify**: exact paths. Say which are new.
4. **Interfaces to honor**: paste the relevant Protocol / DDL / config schema verbatim from the spec. Never paraphrase an interface.
5. **Invariants** (pick those that apply): UTC storage, `as_of` on every feature row, `idempotency_key` on every order, no trade keys outside `riskgate`, paper is default, `features.py` is the single feature module, `mode` is never inferred — always explicit.
6. **Tests that must pass**: pytest/Playwright names and what each asserts. Minimum one failure-path test (bad input, dropped connection, stale data).
7. **Acceptance criteria**: 3–6 checkable bullets. "Ledger page renders empty state with zero rows" not "Ledger works".
8. **Out of scope**: what Cursor must NOT touch this step (usually riskgate, secrets, live mode).
9. **Done signal**: the exact command(s) Ross runs to verify (`docker compose up`, `pytest -q`, URL to open).

## Rules
- One step per prompt. If the step needs >8 files, split it.
- No placeholders like "add appropriate tests". Name them.
- Never ask Cursor to create or read secrets; reference env var names only.
- If the step touches `riskgate/`, `executor/`, or `adapters/`, append: "Run the edge-risk-gate-review checklist before reporting done."
- End with the **receipt contract**: "Report back in this exact format — `files:` list · `tests:` command + pasted output · `assumptions:` list · `touched_gate: yes/no` · `touched_web: yes/no` · `touched_features: yes/no`." The three flags route the diff to the right review skills.
- Include a **budget line**: max files, max new dependencies (default 0), and "stop and report if the step exceeds this."

## Output & handoff
- Write the result to `docs/prompts/{nn}-{slug}.md`. Include: skill name, inputs (commit/PR/model_version/venue), verdict, evidence table, and `next:` line.
- Append one `changelog` row (actor=<skill>, action, before/after if any, reason=<path to the file>).
- Hands off: Cursor builds → receipt → edge-risk-gate-review (if gate/executor/adapters) → edge-ux-review (if apps/web) → edge-leakage-check (if features/backtest/models)
- Evidence rows are `claim | file:line or URL | PASS/FAIL/WARN`. No claim without a location.
