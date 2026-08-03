# Data Guide — Quantum-Safe Cryptography Migration Agent (Stream 3)

---

## 1. NIST Post-Quantum Standards (normative references)

| FIPS | Algorithm | Role |
|---|---|---|
| FIPS 203 | ML-KEM (Kyber) | Key encapsulation / general encryption |
| FIPS 204 | ML-DSA (Dilithium) | Primary digital signatures |
| FIPS 205 | SLH-DSA (SPHINCS+) | Stateless hash-based signatures |

- Announcement: https://www.nist.gov/news-events/news/2024/08/nist-releases-first-3-finalized-post-quantum-encryption-standards
- Transition guidance: NIST IR 8547 (search on csrc.nist.gov)

These are **specifications**, not tabular ML datasets — your agent should encode their parameter sets and migration mappings.

---

## 2. AutoPQC — Synthetic Enterprise Cryptographic Estates

- **IEEE DataPort:** https://ieee-dataport.org/documents/autopqc-synthetic-enterprise-cryptographic-estates-and-post-quantum-migration-planning  
- **Code:** https://github.com/srikanthlumen-bot/autopqc-planner  
- **Why synthetic:** Real enterprise crypto graphs are confidential (they are attacker roadmaps).
- **Contents:** Seeded, reproducible estate generators + migration-planning benchmark results (`results_tight.json`, `results_loose.json`) under multiple planners/baselines.
- **Formats:** Python generator scripts + JSON result files; estates reconstructed from seeds.

```bash
git clone https://github.com/srikanthlumen-bot/autopqc-planner.git raw/autopqc-planner
cd raw/autopqc-planner
# Follow repo README to generate estates from seeds and reproduce planning baselines.
```

---

## 3. PQC-MFB — Post-Quantum Migration Failure Benchmark

- **Dataset:** https://huggingface.co/datasets/nickh007/pqc-mfb  
- **Tooling:** https://github.com/nickharris808/pqc-mfb  
- **What:** 322 cases across 39 failure families for scoring migration robustness.
- **Format:** Structured benchmark records (see HF dataset card) + Python scorer.

```bash
pip install datasets
python -c "from datasets import load_dataset; ds=load_dataset('nickh007/pqc-mfb'); print(ds)"
```

---

## 4. Sample Inventory for Local Hacking (bundled schema)

Create your own JSON CBOM-like inventory if AutoPQC clone is slow:

```json
{
  "assets": [
    {"id": "api-gateway", "algo": "RSA-2048", "protocol": "TLS", "criticality": "high", "deps": ["hsm-1"]},
    {"id": "hsm-1", "algo": "ECDSA-P256", "protocol": "signing", "criticality": "critical", "deps": []},
    {"id": "iot-fleet", "algo": "ECDH-P256", "protocol": "MQTT-TLS", "criticality": "medium", "deps": ["api-gateway"]}
  ]
}
```

Suggested path: `data/raw/sample_estate.json` (the starter agent can generate this automatically).

---

## Mapping Cheat Sheet

| Classical | Risk | NIST-oriented replacement |
|---|---|---|
| RSA key transport / TLS KX | Critical | ML-KEM-768 (often hybrid with X25519 during transition) |
| ECDSA / RSA signatures | High | ML-DSA (Dilithium) or SLH-DSA where hash-based is required |
| ECDH | Critical | ML-KEM / hybrid KEM |

---

## Suggested Local Layout

```
data/
├── README.md
└── raw/
    ├── sample_estate.json
    ├── autopqc-planner/
    └── pqc-mfb/
```
