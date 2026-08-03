# Case 1 — Autonomous Protein-Structure-to-Toxicity Screening Agent

**Stream:** Life Sciences & Bio-Engineering  
**Event:** IEEE YP Industry Hackathon — Autonomous Intelligence for Industrial Innovation  
**Dates:** October 2–4, 2026 | InceptionU, Calgary, Alberta

---

## Problem Statement & Core Challenge

Toxicological profiling of new compounds still bottlenecks drug and chemical development. Modern pipelines can close a **wet-lab ↔ dry-lab loop**: structural biology context (PDB / AlphaFold) informs target relevance, while high-throughput screens (Tox21 / ToxCast) provide bioactivity labels for predictive models.

**Your challenge:** Build an **autonomous agent** that retrieves protein structure context, links compounds to Tox21/ToxCast assays, trains or applies predictive toxicity models, and iteratively proposes which compounds / assays / targets to test next — not a single offline classifier without a decision loop.

---

## Industrial Significance

- Tox21 is a multi-agency U.S. federal program (EPA, NIEHS, NCATS, FDA) aimed at faster, more human-relevant toxicity testing and reduced animal use.
- AlphaFold DB provides >200 million predicted structures, collapsing wait times for structural context.
- Pharma, agrochemical, and consumer-chemical industries need agents that triage large libraries before expensive wet assays.
- Calgary’s life-sciences and health-innovation community can prototype decision agents that generalize to real screening portfolios.

---

## What to Solve For / Technical Objectives

1. **Perceive:** Load Tox21/ToxCast bioactivity tables (and optional PubChem assay links); fetch example PDB / AlphaFold structures for a target class.
2. **Represent:** Featurize compounds (RDKit fingerprints / descriptors) and optionally protein pockets / sequences.
3. **Predict:** Multi-task or selected-assay toxicity classifiers / regressors (DeepChem or sklearn baselines).
4. **Act & Iterate:** Active-learning style loop — select uncertain or high-risk compounds for “virtual wet-lab” evaluation, update the model, re-rank.
5. **Report:** Ranked risk lists with assay rationale and structural context links (PDB ID / UniProt / AlphaFold accession).

---

## Recommended Agent Architecture & Starter Code Pointers

```
Structures (PDB/AF) + Tox assays -> Featurize -> Model -> Acquisition policy -> Updated shortlist
```

**Starter frameworks (open source):**
- [RCSB PDB](https://www.rcsb.org/) — experimental structures (PDB format)
- [AlphaFold DB](https://alphafold.ebi.ac.uk/) — predicted structures (CC-BY-4.0); GCS bulk: `gs://public-datasets-deepmind-alphafold-v4`
- [EPA ToxCast / Tox21 downloads](https://www.epa.gov/comptox-tools/exploring-toxcast-data) and [CompTox downloadable data](https://www.epa.gov/comptox-tools/downloadable-computational-toxicology-data)
- BioPython, RDKit, DeepChem, ColabFold (for on-demand folding if needed)

**In this folder:** `agent_starter.py`, `requirements.txt`, `data/README.md`.

```bash
python -m venv .venv
source .venv/bin/activate   # Windows: .venv\Scripts\activate
pip install -r requirements.txt
python agent_starter.py --help
```

**Requires Python 3.10+.** RDKit / BioPython are optional next steps (see `requirements.txt`).

---

## Success Criteria & Quantitative Evaluation Metrics

| Metric | Target / Guidance |
|---|---|
| Assay prediction AUROC / AUPRC | Report on held-out Tox21-style labels |
| Calibration | Reliability of high-risk scores |
| Active learning gain | Improvement vs. random acquisition over iterations |
| Structure linkage | ≥1 demonstrated PDB/AlphaFold fetch integrated into the narrative |
| Autonomy | Closed propose → (virtual) test → update loop |
| Ethics / safety | No wet-lab instructions for synthesizing hazardous agents; stay on public screening data |

See [JUDGING_RUBRIC.md](../../JUDGING_RUBRIC.md).
