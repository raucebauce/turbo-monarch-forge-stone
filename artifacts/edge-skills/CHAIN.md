# Skill chain (v2)

```
edge-platform-verify ──GO──► edge-adapter-builder ──► edge-risk-gate-review ──► edge-release(A)
        │ DEEP-LINK-ONLY ──► edge-cursor-prompt (deep-link adapter) ──┘
        └ NO-GO ──► changelog, stop

edge-source-onboard ──feature──► edge-feature-spec ──► edge-leakage-check ──► weekly retrain
                    └─claim────► edge-nightly-audit (scores after n≥30)

edge-cursor-prompt ──► Cursor builds ──receipt flags──► risk-gate-review / ux-review / leakage-check ──► edge-release(A)

Parlay Lab output ──► edge-parlay-check ──► shown or rejected

Analyst prompt change ──► edge-reason-card-eval (7-day shadow) ──► nightly-audit applies w

Nightly 04:10 ET: edge-nightly-audit ──gate met──► Ross ──► edge-paper-sim-check ──► edge-release(B) ──► Ross long-press
Weekly Mon 06:00 ET: edge-improve-app ──► issues ──► Ross approves ──► edge-cursor-prompt ──► reviews ──► release(A)

Weekly Mon 06:30 ET + after incidents: edge-skill-forge ──draft + 7-day shadow──► PR ──► Ross approves ──► loaded, CHAIN.md updated

Anything on fire ──► edge-incident (kill switch first, diagnosis second)
```

Every skill writes a file under `docs/` and a `changelog` row. No verdict without `file:line` or URL evidence.
