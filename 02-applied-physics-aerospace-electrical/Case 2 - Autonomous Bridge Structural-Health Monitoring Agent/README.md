# Case 2 — Autonomous Bridge Structural-Health Monitoring Agent

**Stream:** Applied Physics, Aerospace & Electrical Engineering  
**Event:** IEEE YP Industry Hackathon — Autonomous Intelligence for Industrial Innovation  
**Dates:** October 2–4, 2026 | InceptionU, Calgary, Alberta

---

## Problem Statement & Core Challenge

Civil infrastructure degrades progressively under traffic, weather, and fatigue. Detecting and classifying **progressive structural damage** from multi-sensor vibration streams — and prioritizing inspections in a closed loop — is a core hard-science SHM (structural health monitoring) problem.

**Your challenge:** Build an **autonomous agent** that ingests accelerometer vibration from a bridge (or synthetic equivalent), extracts frequency-domain and statistical features, classifies damage scenarios, and iteratively revises alert thresholds / inspection priorities — not a static notebook with a single offline fit.

---

## Industrial Significance

- Bridge failures and deferred maintenance create safety risk, traffic disruption, and multi-billion-dollar remediation costs worldwide.
- The KU Leuven **Z24 bridge** dataset is a landmark benchmark: progressive damage introduced through controlled demolition of a real Swiss highway bridge (1998).
- Multi-sensor vibration SHM patterns transfer directly to wind turbines, pipelines, rail infrastructure, and aerospace panel monitoring.
- Alberta’s civil / energy infrastructure sector benefits from transferable autonomous SHM agent workflows.

---

## What to Solve For / Technical Objectives

1. **Perceive:** Ingest multi-channel accelerometer time series (`inputs.npy`) and scenario labels (`labels.npy`) from the Z24 processed dataset — or synthetic vibration with progressive damage labels.
2. **Diagnose:** Extract FFT / RMS / band-energy features; classify damage scenario (healthy → progressive damage stages).
3. **Prioritize:** Rank segments / sensor setups by anomaly score for field inspection.
4. **Act & Iterate:** Agent proposes alert thresholds and re-scores after each revision; evaluate precision/recall vs. held-out labels.
5. **Stretch:** Cross-setup generalization (9 sensor configurations), uncertainty calibration, or digital-twin modal updating.

---

## Recommended Agent Architecture & Starter Code Pointers

```
Accelerometer streams  ->  Feature encoder (FFT/RMS)  ->  Damage classifier  ->  Inspection priority
              ^                              |                         |
              +-------- re-score after threshold revision -------------+
```

**Starter frameworks (open source):**
- Hugging Face [Z24-dataset-processed](https://huggingface.co/datasets/duan908/Z24-dataset-processed) (cite KU Leuven / original papers)
- Original Z24 campaign: Maeck & De Roeck (2003); Reynders et al. (2008)
- scikit-learn / PyTorch for vibration classification and anomaly detection

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
| Damage classification accuracy / F1 | Report per scenario and macro-averaged |
| Healthy vs. damaged AUC | Binary collapse of progressive stages |
| Inspection priority ranking | NDCG or precision@k on worst-damage segments |
| Alert calibration | Stable alert rate after iterative threshold tuning |
| Autonomy | Closed-loop propose → evaluate → revise on held-out segments |
| Practicality | Demo trains/infers within hackathon compute limits (~1 GB RAM) |

See [JUDGING_RUBRIC.md](../../JUDGING_RUBRIC.md).
