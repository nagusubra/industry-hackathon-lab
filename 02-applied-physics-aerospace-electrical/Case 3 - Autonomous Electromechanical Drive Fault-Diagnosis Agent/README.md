# Case 3 — Autonomous Electromechanical Drive Fault-Diagnosis Agent

**Stream:** Applied Physics, Aerospace & Electrical Engineering  
**Event:** IEEE YP Industry Hackathon — Autonomous Intelligence for Industrial Innovation  
**Dates:** October 2–4, 2026 | InceptionU, Calgary, Alberta

---

## Problem Statement & Core Challenge

Electromechanical drives — motors, gearboxes, and bearings — fail unpredictably under varying load and speed. Diagnosing **bearing faults** by fusing **motor current** and **vibration** signatures across operating conditions is a classic hard-science PHM problem.

**Your challenge:** Build an **autonomous agent** that ingests dual sensor streams, classifies bearing health states, and iteratively revises diagnostic thresholds / load-condition policies — not a static notebook with a single offline fit.

---

## Industrial Significance

- Bearing failures are a leading cause of unplanned downtime in manufacturing, mining, wind turbines, and electric vehicles.
- The Paderborn University **KAt Bearing Data Center** is a widely cited benchmark with 32 bearing states under four operating conditions.
- Fusing electrical (current) and mechanical (vibration) signals mirrors industrial condition-monitoring architectures.
- Alberta’s energy, manufacturing, and EV supply-chain sectors benefit from transferable fault-diagnosis agent patterns.

---

## What to Solve For / Technical Objectives

1. **Perceive:** Ingest motor current + vibration time series from Paderborn `.mat` files — or synthetic dual streams with fault labels.
2. **Diagnose:** Extract time/frequency features; classify healthy vs. inner/outer race / cage faults.
3. **Fuse:** Combine current and vibration modalities (early/late fusion, attention, or ensemble).
4. **Act & Iterate:** Agent revises decision thresholds per load condition (1500/900 rpm × 0.7 / 0.1 / 0.4 Nm); re-evaluate F1 / confusion matrix.
5. **Stretch:** Cross-condition generalization, few-shot transfer, or real-time edge deployment.

---

## Recommended Agent Architecture & Starter Code Pointers

```
Current + Vibration  ->  Feature extractors  ->  Fault classifier  ->  Condition-aware policy
         ^                          |                      |
         +-------- re-score after threshold revision -------+
```

**Starter frameworks (open source):**
- [Paderborn KAt Bearing Data Center](https://mb.uni-paderborn.de/kat/forschung/bearing-datacenter)
- [Zenodo mirror](https://zenodo.org/records/15845309)
- Cite: Lessmeier et al., PHM Society Europe 2016

**License:** CC BY-NC 4.0 — non-commercial use only. Verify terms before any commercial deployment.
- scikit-learn / PyTorch for signal classification

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
| Fault classification accuracy / macro-F1 | Report per condition and averaged |
| Healthy vs. faulty AUC | Binary collapse of damage classes |
| Cross-condition robustness | Train on 2 conditions, test on held-out 2 |
| Alert calibration | Stable detection rate after iterative tuning |
| Autonomy | Closed-loop propose → evaluate → revise per load condition |
| Practicality | Demo uses 2–4 `.mat` files (~170 MB each), not full multi-GB corpus |

See [JUDGING_RUBRIC.md](../../JUDGING_RUBRIC.md).
