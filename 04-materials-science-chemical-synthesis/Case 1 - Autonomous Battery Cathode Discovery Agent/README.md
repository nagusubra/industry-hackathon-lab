# Case 1 — Autonomous Battery Cathode Discovery Agent

**Stream:** Materials Science & Chemical Synthesis  
**Event:** IEEE YP Industry Hackathon — Autonomous Intelligence for Industrial Innovation  
**Dates:** October 2–4, 2026 | InceptionU, Calgary, Alberta

---

## Problem Statement & Core Challenge

Discovering battery electrode materials requires navigating a vast chemical space under competing objectives: voltage, gravimetric/volumetric capacity, energy density, thermodynamic stability, earth abundance, and toxicity. Manual browsing of databases does not scale.

**Your challenge:** Build an **autonomous materials agent** that queries the Materials Project, proposes cathode / insertion-electrode candidates, scores multi-objective trade-offs, and iteratively refines search constraints using `pymatgen` / `mp-api` — a closed discovery loop, not a one-shot chatbot answer.

---

## Industrial Significance

- Electrification of transport and grid storage depends on better, cheaper, more sustainable cathodes.
- High-throughput DFT databases (Materials Project) already encode thousands of insertion electrodes ready for ML + agentic search.
- Alberta’s energy transition and Canada’s critical-minerals strategy make battery materials R&D regionally strategic.
- Agents that respect stability and resource constraints reduce wasted wet-lab cycles.

---

## What to Solve For / Technical Objectives

1. **Perceive:** Pull insertion-electrode documents via Materials Project API (`mp-api`) — voltage, capacity, energy density, working ion, stability proxies.
2. **Featurize:** Use `pymatgen` structures / compositions for descriptors (elemental properties, structural fingerprints).
3. **Search:** Multi-objective selection (e.g., Pareto front on energy density vs. stability vs. critical-element penalties).
4. **Act & Iterate:** Agent updates query filters / generative proposals based on scored shortlists; optional MatGL property models for surrogates.
5. **Report:** Ranked candidates with MP IDs, predicted metrics, and rationale suitable for a materials engineer.

---

## Recommended Agent Architecture & Starter Code Pointers

```
MP API query -> pymatgen featurize -> multi-objective rank -> constraint update -> re-query
```

**Starter frameworks (open source):**
- [Materials Project API docs](https://docs.materialsproject.org/downloading-data/using-the-api/getting-started)
- [`mp-api`](https://github.com/materialsproject/api) / `MPRester`
- [`pymatgen`](https://github.com/materialsproject/pymatgen)
- Optional: [MatGL](https://github.com/materialsvirtuallab/matgl) graph deep learning; ASE for atomistic workflows

**In this folder:** `agent_starter.py`, `requirements.txt`, `data/README.md`.

```bash
python -m venv .venv
source .venv/bin/activate   # Windows: .venv\Scripts\activate
export MP_API_KEY=your_key_here   # Windows PowerShell: $env:MP_API_KEY="..."
pip install -r requirements.txt
python agent_starter.py --help
```

**Requires Python 3.10+.**

---

## Success Criteria & Quantitative Evaluation Metrics

| Metric | Target / Guidance |
|---|---|
| Candidate quality | Shortlist with energy density / voltage / capacity reported from MP fields |
| Stability filter | Prefer electrodes within documented stability windows when available |
| Critical element penalty | Explicit scoring for Co/Ni/etc. abundance or supply-risk heuristics |
| Pareto coverage | Non-dominated set size and diversity across chemistries |
| Autonomy | ≥1 iteration where filters change based on prior shortlist statistics |
| Reproducibility | Seeded queries + saved JSON shortlist artifacts |

See [JUDGING_RUBRIC.md](../../JUDGING_RUBRIC.md).
