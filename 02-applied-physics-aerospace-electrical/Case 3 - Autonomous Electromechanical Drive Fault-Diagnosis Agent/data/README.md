# Data Guide — Electromechanical Drive Fault-Diagnosis Agent (Stream 2)

---

## Primary Dataset: Paderborn University KAt Bearing Data Center

- **Portal:** https://mb.uni-paderborn.de/kat/forschung/bearing-datacenter  
- **Zenodo mirror:** https://zenodo.org/records/15845309  
- **License:** CC BY-NC 4.0 (non-commercial)  
- **Format:** MATLAB `.mat` files inside `.rar` archives (~170 MB each)  
- **Content:** 32 bearing states (healthy + artificially damaged) × 4 operating conditions  
- **Signals:** Motor current (1 channel) + vibration (2 channels) at 64 kHz, 4 s duration

### Operating Conditions

| Code | Speed | Torque |
|---|---|---|
| N15_M07_F10 | 1500 rpm | 0.7 Nm |
| N09_M07_F10 | 900 rpm | 0.7 Nm |
| N15_M01_F10 | 1500 rpm | 0.1 Nm |
| N15_M07_F04 | 1500 rpm | 0.4 Nm |

### Citation

Lessmeier, C., et al. (2016). *Condition Monitoring of Bearing Damage in Electromechanical Drive Systems by Using Motor Current Signals of Electric Motors: A Benchmark Data Set for Data-Driven Classification.* PHM Society European Conference.

---

## Download Steps

1. Open the [Paderborn bearing datacenter](https://mb.uni-paderborn.de/kat/forschung/bearing-datacenter) **or** the [Zenodo record](https://zenodo.org/records/15845309).

2. Download **1–2 healthy** and **1–2 damaged** `.mat` / `.rar` files (~170 MB each). **Do not download the full multi-GB corpus** — a handful of bearings is sufficient for the hackathon.

3. Extract and place files under `data/raw/paderborn/`:

```bash
mkdir -p data/raw/paderborn
# Example after downloading K001.rar and KA04.rar locally:
unrar x K001.rar data/raw/paderborn/
unrar x KA04.rar data/raw/paderborn/
```

**Windows:** use [7-Zip](https://www.7-zip.org/) to extract `.rar` archives if `unrar` is unavailable.

**Official `.mat` format:** Paderborn files store signals in nested MATLAB structs (e.g. key `Y` for vibration). They require custom parsing — see the [Paderborn datacenter documentation](https://mb.uni-paderborn.de/kat/forschung/bearing-datacenter). The starter agent writes **synthetic** `.mat` files with flat `current` / `vibration` keys so `agent_starter.py` runs immediately without a parser.

### Loading Example

```python
import scipy.io as sio
from pathlib import Path

mat = sio.loadmat("data/raw/paderborn/K001/N15_M07_F10_K001_1.mat", squeeze_me=True)
# Official files: inspect keys — vibration is under 'Y' (nested struct)
# Synthetic demo files: flat keys 'current', 'vibration', 'fault_label'
print([k for k in mat.keys() if not k.startswith("__")])
```

---

## Suggested Local Layout

```
data/
├── README.md
└── raw/
    └── paderborn/
        ├── K001/          # healthy example
        └── KA04/          # damaged example
```
