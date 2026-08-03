# Case 1 — Autonomous Quantum-Safe Cryptography Migration Agent

**Stream:** Software, Cryptography & Computational Math  
**Event:** IEEE YP Industry Hackathon — Autonomous Intelligence for Industrial Innovation  
**Dates:** October 2–4, 2026 | InceptionU, Calgary, Alberta

---

## Problem Statement & Core Challenge

Cryptographically relevant quantum computers threaten RSA/ECC. NIST has finalized post-quantum standards (**FIPS 203 ML-KEM**, **FIPS 204 ML-DSA**, **FIPS 205 SLH-DSA**). Enterprises must inventory quantum-vulnerable cryptography and plan sequenced migrations under dependency, budget, and downtime constraints — a combinatorial planning problem, not a slide deck.

**Your challenge:** Build an **autonomous agent** that discovers classical crypto usage (code / CBOM / synthetic estate graphs), maps findings to NIST PQC replacements, simulates migration waves, and iteratively repairs plans against failure modes — beyond “chat about Kyber.”

---

## Industrial Significance

- CNSA 2.0 / federal and critical-infrastructure timelines make PQC migration a dated compliance requirement.
- Real crypto inventories are sensitive; synthetic estates (AutoPQC) enable reproducible research without leaking attack maps.
- Incorrect migrations fail in subtle ways (header limits, hybrid negotiation, performance regressions) — see PQC-MFB failure families.
- Canadian critical infrastructure and Alberta energy/OT environments increasingly need crypto-agility roadmaps.

---

## What to Solve For / Technical Objectives

1. **Perceive:** Ingest a synthetic cryptographic estate or scan a sample codebase for RSA/ECC/TLS usage.
2. **Classify:** Map each finding to NIST FIPS 203/204/205 algorithms and risk tiers.
3. **Plan:** Produce a staged migration schedule respecting dependencies and budgets (QUBO / ILP / heuristic planner).
4. **Validate:** Benchmark candidate KEMs/signatures via liboqs / `oqs` Python bindings; score plans against PQC-MFB-style failure checks where applicable.
5. **Iterate:** Agent revises the plan when simulations detect dependency violations, over-budget stages, or known failure families.

---

## Recommended Agent Architecture & Starter Code Pointers

```
Inventory / CBOM -> Risk graph -> Migration planner -> liboqs benchmarks -> Revised plan
```

**Starter frameworks (open source):**
- NIST PQC standards: https://www.nist.gov/news-events/news/2024/08/nist-releases-first-3-finalized-post-quantum-encryption-standards
- [Open Quantum Safe liboqs](https://github.com/open-quantum-safe/liboqs) + `oqs` Python package
- [pqc-migrator](https://github.com/BasitS-hash/pqc-migrator) — readiness scanner / CBOM
- [AutoPQC planner](https://github.com/srikanthlumen-bot/autopqc-planner) + IEEE DataPort synthetic estates
- [PQC-MFB](https://huggingface.co/datasets/nickh007/pqc-mfb) — migration failure benchmark
- Optional: [Qiskit](https://github.com/Qiskit/qiskit) for didactic Shor-threat demonstrations (not a substitute for PQC engineering)

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
| Inventory coverage | % of synthetic estate nodes classified with NIST mapping |
| Plan feasibility | Zero dependency violations; stages within budget |
| Risk coverage | Stages to ≥90% risk reduction (AutoPQC-style) |
| Crypto performance | ML-KEM / ML-DSA handshake or encapsulate latency vs. classical baseline (liboqs) |
| Failure awareness | Explicit checks against ≥1 PQC-MFB failure family |
| Autonomy | Planner revises after simulated constraint violation |

See [JUDGING_RUBRIC.md](../../JUDGING_RUBRIC.md).
