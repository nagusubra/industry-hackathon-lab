# Data Guide — Battery Health and RUL Agent (Stream 2)

---

## Primary Dataset: NASA PCoE Li-ion Battery Aging

- **Portal:** https://data.nasa.gov/dataset/li-ion-battery-aging-datasets  
- **Direct zip:** https://phm-datasets.s3.amazonaws.com/NASA/5.+Battery+Data+Set.zip  
- **License:** Public domain / US Government Works (NASA PCoE dataset — no copyright restrictions on US Government works)  
- **Format:** MATLAB `.mat` files (~34 cells)  
- **Content:** Charge/discharge cycles, capacity measurements, impedance (EIS) for 18650 Li-ion cells aged under controlled conditions

### Typical Variables (per cell `.mat`)

| Field | Description |
|---|---|
| `cycle` | Struct array of charge/discharge/EIS cycles |
| `data.Voltage_measured` | Terminal voltage (V) |
| `data.Current_measured` | Current (A) |
| `data.Temperature_measured` | Temperature (°C) |
| `data.Capacity` | Discharge capacity (Ah) |

End-of-life is commonly defined at 70% of initial rated capacity (~2.0 Ah for these cells).

### Citation

Saha, B., & Goebel, K. (2007). *Battery Data Set.* NASA Ames Prognostics Center of Excellence (PCoE). https://data.nasa.gov/dataset/li-ion-battery-aging-datasets

---

## Download Steps

1. Download the zip from the S3 URL above **or** from the [NASA Open Data portal](https://data.nasa.gov/dataset/li-ion-battery-aging-datasets).

2. Unzip into `data/raw/nasa-battery/`:

```bash
mkdir -p data/raw/nasa-battery
# After downloading "5. Battery Data Set.zip" locally:
unzip "5. Battery Data Set.zip" -d data/raw/nasa-battery
```

3. Load with `scipy.io.loadmat`:

```python
import scipy.io as sio
from pathlib import Path

mat = sio.loadmat("data/raw/nasa-battery/B0005.mat", squeeze_me=True)
cycle = mat["cycle"]
print(type(cycle), len(cycle))
```

### Optional: Randomized Battery Usage (Zenodo)

For additional cycling diversity, see [Randomized Battery Usage Dataset on Zenodo](https://zenodo.org/records/10668737). Download only the cells you need. **Check the Zenodo record license** before use — terms may differ from the NASA PCoE public-domain dataset.

---

## Suggested Local Layout

```
data/
├── README.md
└── raw/
    └── nasa-battery/
        ├── B0005.mat
        ├── B0006.mat
        └── ...
```
