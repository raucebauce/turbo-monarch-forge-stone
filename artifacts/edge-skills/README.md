# EDGE skills — v2.1 (16 skills)

Add to Grok: Skills → Add Skill → each SKILL.md. Reference by name in prompts. See CHAIN.md for how they hand off to each other.

| Skill | When |
|---|---|
| edge-platform-verify | Before any venue key or adapter |
| edge-source-onboard | Before consuming any new feed, subreddit, Discord, capper, news API |
| edge-cursor-prompt | Every time code needs writing |
| edge-adapter-builder | Building a venue adapter |
| edge-feature-spec | Adding a model input |
| edge-risk-gate-review | Any diff touching gate/executor/adapters/mode/agent tool scopes |
| edge-leakage-check | Before trusting any ROI/CLV/accuracy number |
| edge-paper-sim-check | Before any paper→live flip; after simulator changes |
| edge-parlay-check | Every Parlay Lab output before display |
| edge-reason-card-eval | Weekly; any Analyst prompt change |
| edge-ux-review | Before a screen ships |
| edge-nightly-audit | 04:10 ET daily, or interpreting Auditor output |
| edge-improve-app | Monday 06:00 ET, app-health loop |
| edge-release | Deploys (A) and paper→live flips (B) |
| edge-skill-forge | Weekly, after incidents, or "make this a skill" — the system drafts/upgrades its own skills; Ross approves the PR |
| edge-incident | Reconciliation mismatch, runaway orders, outage, key compromise, unexpected live loss |

v2 changes: every skill now has an Output & handoff section (file path, changelog row, next skill, evidence format); cursor-prompt has a receipt contract with routing flags and a budget line; nightly-audit handles postponed games, pending_external picks, and agent cost guard; release adds simulator validation and a 48h live warm-up at half caps; risk-gate-review adds the agent-boundary check; five new skills fill the gaps (source onboarding, paper-sim validation, incident, reason-card eval, parlay check).
