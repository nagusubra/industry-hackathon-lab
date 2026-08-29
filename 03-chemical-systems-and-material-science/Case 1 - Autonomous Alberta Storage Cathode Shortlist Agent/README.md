# Case 1 — Autonomous Alberta Storage Cathode Shortlist Agent

**Stream:** Chemical Systems and Material Science  
**Event:** IEEE YP Industry Hackathon — Autonomous Intelligence for Industrial Innovation  
**Dates:** October 2–4, 2026 | InceptionU, Calgary, Alberta

---

## Problem Statement & Core Challenge

Alberta is adding **grid batteries** so wind and solar can be stored when the pool price is low. Battery teams still have to pick a cathode chemistry: high energy is good; unstable or rare-element recipes are not.

You will not call a materials API and you will not run a lab. You will use a **table of already-computed properties** and produce a shortlist a storage developer can argue about.

**Your challenge:** From a cathode properties CSV, output a **top 10**. Beat “sort by energy density only.” Then change one filter (minimum voltage, or ban a critical element) and show how the top 10 changes.

---

## Industrial Significance

- AESO’s market is energy-only and volatile; storage is a local industrial story (YEIP, utilities, developers).
- **Who would use this:** a storage developer or Alberta materials startup doing first-pass screening. **What is sold:** a transparent shortlist, not a magic “best battery.”

---

## What to Solve For / Technical Objectives

1. **Perceive:** Load the electrode table (voltage, capacity, energy, stability, working ion, formula). Drop incomplete rows.
2. **Reason:** Score with at least two objectives (e.g. energy density **and** a penalty for listed critical elements). Write the score in one line.
3. **Act:** Top 10 with reasons. Baseline = sort by gravimetric energy only.
4. **Iterate:** Raise minimum voltage **or** exclude Co/Ni (you choose); re-rank.
5. **Explain:** What you would tell a chemist vs what you would tell a project financier.

Stretch: plot a simple Pareto (energy vs stability) and pick the knee.

---

## Recommended Architecture

```
┌─────────────┐    ┌──────────────┐    ┌────────────────┐    ┌─────────────┐
│  Perceive   │ -> │   Score      │ -> │  Top 10        │ -> │  Change     │
│ cathode CSV │    │ energy minus │    │ vs energy-only │    │ one filter  │
│             │    │ penalties    │    │                │    │             │
└─────────────┘    └──────────────┘    └────────────────┘    └─────────────┘
```

Run [`agent_starter.py`](agent_starter.py). See [`data/README.md`](data/README.md). **No Materials Project API key** for this case.

**Requires Python 3.10+ (3.11 recommended).**

---

## Success Criteria & Quantitative Evaluation Metrics

| Metric | Target / Guidance |
|---|---|
| Baseline | Top 10 by energy density (or capacity) alone |
| Your list | Overlap vs baseline + why the new names appeared |
| Loop | ≥ 1 filter/weight change |
| Provenance | Keep formula / id from the source table |
| Honesty | These are database values, not lab-validated cells |

See [JUDGING_RUBRIC.md](../../JUDGING_RUBRIC.md).
