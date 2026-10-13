---
name: edge-skill-forge
description: "EDGE writes its own skills. Detects a recurring procedure, gap, or incident lesson, drafts a new SKILL.md or an upgrade to an existing one, shadow-tests it, and proposes it as a PR. Ross approves; nothing self-installs. Runs weekly and after every incident."
type: workflow
lifecycle: active
---
# Skill forge (self-directed skill creation)

The system may author procedures for itself. It may not grant itself permissions.

## Triggers
- Weekly (Mon 06:30 ET, after edge-improve-app).
- After any edge-incident postmortem.
- When the Orchestrator performs the same ad-hoc multi-step sequence ≥3 times in 14 days (detected from `changelog` actor/action patterns).
- When a skill's verdict was overturned by later evidence ≥2 times (e.g., PASS then incident) — the skill is missing a check.
- When Ross says "make this a skill."

## Inputs
`changelog`, `docs/incidents/`, `docs/reviews/`, `docs/IMPROVE_ME.md`, agent transcripts (logged), and the current `edge-skills/` set with CHAIN.md.

## Procedure
1. **Name the gap** in one sentence: what kept happening, what it cost, which existing skill should have caught it (or none).
2. **Decide new vs. upgrade.** Upgrade if an existing skill's scope covers it; new only if no skill owns the trigger. Never fork a skill into two overlapping ones.
3. **Draft** using the house format: frontmatter (`name`, `description` with when-to-use), sections for triggers/inputs/procedure/tests or checks, and the mandatory **Output & handoff** block (docs path, changelog row, next skill, evidence format). ≤120 lines. Every check must be verifiable with `file:line`, a URL, or a query.
4. **Lint against the guardrail list** (below). A draft that touches any item is rejected before shadow.
5. **Shadow-run** 7 days: the draft runs alongside the current skill (or alongside nothing, for new), writes to `docs/reviews/shadow/`, never gates anything. Measure: would it have changed a verdict, caught an incident, or saved a step? Count tokens it cost.
6. **Propose**: PR to `edge-skills/` with the SKILL.md, the shadow report, an updated CHAIN.md and README row, and a one-paragraph rationale. Tag `skill-forge`. Push a 3-line summary to Ross.
7. **On approval**: Orchestrator loads it; a `changelog` row records `skill_installed` with the PR link. On rejection: record why in `docs/skills/rejected.md` so it isn't re-proposed for 90 days.

## Self-tuning of existing skills (allowed without a PR)
Only numeric thresholds explicitly marked `tunable:` inside a skill (e.g., staleness seconds, sample sizes) may be adjusted by the Auditor within the stated range, with a changelog row. Any other edit is a PR.

## Guardrails — a draft may never
- Enable live mode, raise any cap, alter risk-gate checks or their order, touch key handling, or merge/deploy code.
- Remove or weaken the Output & handoff block, evidence standard, or any "Ross only" line in an existing skill.
- Grant any agent new tool scopes, or write a skill whose procedure instructs an agent to act outside its role.
- Install itself. Installation is Ross's tap on the PR.
- Modify this skill's guardrail section. Changes here are Ross-authored only.

## Output & handoff
- `docs/skills/{date}-{name}.md` (gap statement, draft, shadow report) + the PR. Changelog row `skill_proposed`.
- Hands off: Ross approves → Orchestrator loads; the new skill's own handoff lines slot it into CHAIN.md.

