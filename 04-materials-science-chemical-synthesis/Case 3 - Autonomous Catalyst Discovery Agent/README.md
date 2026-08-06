# Case 3 — Autonomous Catalyst Discovery Agent

**Stream:** Materials Science & Chemical Synthesis  
**Event:** IEEE YP Industry Hackathon — Autonomous Intelligence for Industrial Innovation  
**Dates:** October 2–4, 2026 | InceptionU, Calgary, Alberta

---

## Problem Statement & Core Challenge

Electrocatalyst discovery for hydrogen evolution (HER), oxygen evolution (OER), and CO₂ reduction (CO₂RR) requires screening adsorption and reaction energies across vast compositional spaces. DFT databases such as **Catalysis-Hub** encode ~158k surface reactions with adsorption energies, but brute-force browsing does not scale.

**Your challenge:** Build an **autonomous catalyst-discovery agent** that queries Catalysis-Hub via GraphQL, scores candidates against **Sabatier-volcano** binding-energy targets, performs multi-objective ranking (activity vs. stability proxies), and **iteratively refines search filters** — mirroring the Materials Project discovery loop in Case 1.

---

## Industrial Significance

- Green hydrogen, fuel cells, and CO₂ electrolysis depend on affordable, durable electrocatalysts (often beyond Pt-group benchmarks).
- Catalysis-Hub aggregates community DFT results for adsorption energies on binary / ternary surfaces.
- Autonomous agents that respect volcano-plot physics reduce wasted supercomputer and wet-lab cycles.
- Alberta’s hydrogen strategy and carbon-management roadmap align with accelerated catalyst screening.

---

## What to Solve For / Technical Objectives

1. **Perceive:** Query Catalysis-Hub GraphQL for adsorption / reaction energies (e.g., *OH, *O, *H, CO*) on metal / alloy surfaces.
2. **Score:** Map adsorption energies to Sabatier-volcano distance from optimal binding (HER ≈ ΔG_H ≈ 0 eV; OER/CO₂RR have family-specific descriptors).
3. **Search:** Multi-objective selection (activity proxy, overbinding/underbinding penalties, optional alloy complexity).
4. **Act & Iterate:** Agent revises element / facet / energy-window filters based on shortlist statistics; re-queries.
5. **Report:** Ranked surfaces with formulas, adsorption energies, volcano scores, and literature DOIs when available.

---

## Recommended Agent Architecture & Starter Code Pointers

```
GraphQL query  ->  adsorption featurize  ->  volcano / multi-objective rank  ->  filter revision  ->  re-query
```

**Starter frameworks (open source):**
- [Catalysis-Hub](https://www.catalysis-hub.org/) — GraphQL endpoint: http://api.catalysis-hub.org/graphql
- ASE / pymatgen for optional structure follow-up
- Literature: Nørskov Sabatier analysis; OER scaling relations (Man et al., Rossmeisl et al.)

**In this folder:** `agent_starter.py`, `requirements.txt`, `data/README.md`.

```bash
python -m venv .venv
source .venv/bin/activate   # Windows: .venv\Scripts\activate
pip install -r requirements.txt
python agent_starter.py --help
```

**Requires Python 3.10+.**

---

## Success Criteria & Quantitative Evaluation Metrics

| Metric | Target / Guidance |
|---|---|
| Volcano proximity | Mean |ΔG − ΔG_opt| for top-k HER/OER candidates |
| Multi-objective coverage | Pareto front size across activity vs. complexity |
| Filter autonomy | ≥1 iteration where GraphQL filters change from prior shortlist |
| Data provenance | DOI / publication fields preserved when returned by API |
| Practicality | Cached subset queryable offline if API is slow during the event |
| Reproducibility | Saved JSON/CSV shortlist artifacts |

See [JUDGING_RUBRIC.md](../../JUDGING_RUBRIC.md).
