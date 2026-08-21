# Case 6 — Autonomous Interconnection-Queue Risk-Triage Agent

**Stream:** Energy Systems & Environmental Modeling  
**Event:** IEEE YP Industry Hackathon — Autonomous Intelligence for Industrial Innovation  
**Dates:** October 2–4, 2026 | InceptionU, Calgary, Alberta

---

## Problem Statement & Core Challenge

U.S. transmission interconnection queues are a binding constraint on new generation and storage. Berkeley Lab’s *Queued Up* series shows that **most queued capacity is withdrawn**, and projects that reach commercial operation often wait **more than five years**. A planner or developer who only plots GW in queue is looking at a dashboard. The industrial problem is **which requests will complete, how long they will take, and how a limited study/upgrade budget should be sequenced**.

**Your challenge:** Build an **autonomous AI agent** that scores withdrawal risk and expected time-to-interconnection for generation/storage requests, then recommends a **prioritized study/portfolio action** for a transmission planner. Evaluate recommendations against **historical outcomes** (operational / withdrawn / still active) on a time-based held-out split — not just classification accuracy.

---

## Industrial Significance

- As of end-2025, ~8,200 active requests represented ~1,312 GW generation and ~749 GW storage; only ~13% of 2000–2020 requests had reached commercial operation by end-2025, while ~75% had been withdrawn (LBNL *Queued Up* 2026).
- This maps directly onto DOE Office of Electricity 2026 priorities: **scaling the system for new load** (data centers, manufacturing), **transmission congestion**, and **affordable reliability**. See the [2026 National Transmission Needs Study](https://www.energy.gov/oe/articles/does-office-electricity-publishes-2026-draft-national-transmission-needs-study) and OE’s strategic plan.
- FERC Order 2023 cluster-study reforms make **risk-aware queue clustering and restudy sequencing** an operator workflow, not a research toy.
- Developers, offtakers, and state energy offices use the same scores to decide which PPAs and interconnection deposits are real.

---

## What to Solve For / Technical Objectives

1. **Perceive:** Load the LBNL project-level interconnection workbook (ISO/RTO + non-ISO balancing areas through 2025) and map codebook fields to technology, capacity, region, queue-entry date, and outcome.
2. **Predict:** Estimate P(withdrawn) and expected months-to-COD (or time-in-queue) with uncertainty. Use a **temporal split** (train on earlier queue-entry cohorts; test on later ones) to avoid leakage.
3. **Decide:** Rank a planner portfolio — e.g. expected completed MW per study-slot, or a constrained budget of N cluster studies — not a unsorted risk list.
4. **Act & Iterate:** Simulate acting on the top-k recommendations; score against realized operational MW / wasted study slots; revise features or ranking weights when calibration is poor.
5. **Explain:** Per-project rationale: region, fuel, size, queue age, and why the agent would study, wait, or deprioritize.

Stretch goals: survival models (Cox / AFT) for time-to-event; calibration plots; ISO-specific models; coupling with a simplified upgrade-cost proxy.

---

## Recommended Agent Architecture & Starter Code Pointers

```
┌─────────────┐    ┌──────────────┐    ┌────────────────┐    ┌─────────────┐
│  Perceive   │ -> │   Reason     │ -> │  Tool / Sim    │ -> │  Act / Log  │
│ queue xlsx  │    │ P(withdraw)  │    │ rank study     │    │ portfolio   │
│ + codebook  │    │ + months COD │    │ slots vs hist. │    │ action      │
└─────────────┘    └──────────────┘    └────────────────┘    └─────────────┘
                              ^                                     |
                              +------------- evaluate --------------+
```

**Starter references:**
- Data + report hub: https://emp.lbl.gov/queues
- *Queued Up: 2026 Edition* (data through 2025): https://emp.lbl.gov/publications/queued-2026-edition-characteristics
- DOE OE Needs Study context: https://www.energy.gov/oe/articles/does-office-electricity-publishes-2026-draft-national-transmission-needs-study

**In this folder:**
- [`agent_starter.py`](agent_starter.py) — risk model + study-slot ranking loop (real workbook or labeled synthetic demo)
- [`requirements.txt`](requirements.txt)
- [`data/README.md`](data/README.md)

```bash
python -m venv .venv
source .venv/bin/activate   # Windows: .venv\Scripts\activate
pip install -r requirements.txt
python agent_starter.py --help
```

**Requires Python 3.10+ (3.11 recommended).**

---

## Success Criteria & Quantitative Evaluation Metrics

| Metric | Target / Guidance |
|---|---|
| Withdrawal ranking | AUROC / PR-AUC vs. majority-class baseline on held-out **entry-year** split |
| Time-to-event | MAE of months-in-queue among completed projects (report coverage) |
| Portfolio value | Completed MW captured in top-k study slots vs. random and vs. “largest-MW-first” |
| Calibration | Reliability of P(withdraw) in deciles (ECE or a calibration plot) |
| Leakage control | No test-year outcomes or post-decision dates in training features |
| Agent loop autonomy | ≥ 1 closed-loop iteration (score → rank → evaluate → reweight) |
| Runtime practicality | End-to-end demo within the 48-hour prototype window |

Judges will prioritize **decision quality under historical outcomes** over a status dashboard. See [JUDGING_RUBRIC.md](../../JUDGING_RUBRIC.md).
