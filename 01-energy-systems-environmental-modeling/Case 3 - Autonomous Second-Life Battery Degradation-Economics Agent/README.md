# Case 3 — Autonomous Second-Life Battery Degradation-Economics Agent

**Stream:** Energy Systems & Environmental Modeling  
**Event:** IEEE YP Industry Hackathon — Autonomous Intelligence for Industrial Innovation  
**Dates:** October 2–4, 2026 | InceptionU, Calgary, Alberta

---

## Problem Statement & Core Challenge

Second-life lithium-ion cells retired from electric vehicles can provide valuable grid-storage capacity, but every charge/discharge cycle accelerates capacity fade. Operators must trade **cycling revenue** (arbitrage, peak shaving, frequency regulation) against **remaining useful life** and replacement economics. A naive "always cycle" policy maximizes short-term revenue but destroys asset value; an overly conservative policy leaves revenue stranded.

**Your challenge:** Build an **autonomous AI agent** that ingests cell cycling data and degradation curves, reasons about state-of-health (SOH) trajectories under different duty cycles, and iteratively proposes (and evaluates) dispatch policies that balance revenue vs. fade — not a static degradation spreadsheet.

---

## Industrial Significance

- Second-life batteries are a cornerstone of circular-economy energy storage, with major automakers and utilities piloting residential and commercial repurposing programs.
- Stanford Energy Control Lab published open cycling data for NMC cells under realistic residential and commercial duty cycles — directly usable for degradation-aware dispatch research.
- Alberta and Canadian grid modernization depends on cost-effective storage; agents that optimize total lifecycle value (not just daily revenue) are industrially relevant.
- Degradation-aware dispatch reduces waste, extends asset life, and improves the business case for second-life storage deployments.

---

## What to Solve For / Technical Objectives

1. **Perceive:** Ingest second-life NMC cell cycling datasets (capacity fade, voltage, current, temperature over residential + commercial duty cycles).
2. **Model:** Fit or apply SOH / capacity-fade models (empirical curves, rainflow counting, or ML surrogates).
3. **Optimize:** Formulate a policy that trades cycle depth, C-rate, and revenue opportunity against predicted fade and replacement cost.
4. **Act & Iterate:** Implement an agent loop that proposes cycling strategies, evaluates lifecycle economics in simulation, and revises when fade exceeds targets.
5. **Explain:** Emit asset-manager summaries: expected remaining life, revenue per cycle, fade cost, and recommended depth-of-discharge limits.

Stretch goals: fleet-level second-life portfolio optimization; temperature-aware fade models; coupling with Alberta/AESO price signals.

---

## Recommended Agent Architecture & Starter Code Pointers

```
┌─────────────┐    ┌──────────────┐    ┌────────────────┐    ┌─────────────┐
│  Perceive   │ -> │   Reason     │ -> │  Tool / Sim    │ -> │  Act / Log  │
│ cycling CSV │    │ SOH forecast │    │ fade + revenue │    │ cycle depth │
│ + fade data │    │ + economics  │    │ lifecycle model│    │ & metrics   │
└─────────────┘    └──────────────┘    └────────────────┘    └─────────────┘
                              ^                                     |
                              +------------- evaluate --------------+
```

**Starter references (open data):**
- [OSF dataset — Second-Life Li-ion Grid Storage Cycling](https://osf.io/8jnr5/) — DOI: 10.17605/OSF.IO/8JNR5
- Moy, A., Khan, M., & Onori, S. (2024). Second-life Li-ion grid storage cycling dataset. *Data in Brief*. https://doi.org/10.1016/j.dib.2024.111046
- File: `SL_Dataset_SECL_INR21700-M50T.zip` — Stanford Energy Control Lab, 6 NMC INR21700-M50T cells

**In this folder:**
- [`agent_starter.py`](agent_starter.py) — perceive / reason / act skeleton wired to local data paths
- [`requirements.txt`](requirements.txt) — core Python dependencies
- [`data/README.md`](data/README.md) — verified dataset links, schemas, and download steps

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
| Lifecycle net present value ($) | Maximize vs. naive full-depth cycling baseline |
| Capacity fade rate (%/cycle) | Report and minimize while meeting revenue targets |
| SOH endpoint at horizon | Stay above operator-defined retirement threshold (e.g., 70% SOH) |
| Revenue per kWh cycled | Report vs. baseline policies |
| Agent loop autonomy | ≥ 1 closed-loop iteration (propose → simulate → revise) without human prompts |
| Runtime practicality | End-to-end demo runnable within the 48-hour prototype window |

Judges will prioritize **degradation physics + economic reasoning + autonomous tool use** over UI polish alone. See [JUDGING_RUBRIC.md](../../JUDGING_RUBRIC.md).
