#!/usr/bin/env python3
"""
IEEE YP Industry Hackathon — Stream 1 Starter Agent
Case: Autonomous Building-Stock Electrification and Retrofit-Prioritization Agent
Event: IEEE YP Industry Hackathon, Oct 2-4 2026, InceptionU Calgary

Allocate a retrofit budget across building segments to maximize
peak and energy savings; compare to greedy; revise weights.
"""

from __future__ import annotations

import argparse
from pathlib import Path
from typing import Any

import numpy as np
import pandas as pd


def _synthesize_segments(path: Path) -> pd.DataFrame:
    """Labeled synthetic segments — not NREL ResStock."""
    path.parent.mkdir(parents=True, exist_ok=True)
    rows = [
        # segment, n_units, cost_per_unit, base_peak_kw, up_peak_kw, base_mwh, up_mwh
        ("CO-single_family_detached-pre1980", 80_000, 14_000, 1.9, 1.35, 14.5, 10.2),
        ("CO-single_family_detached-post1980", 60_000, 11_500, 1.6, 1.25, 12.0, 9.4),
        ("CO-single_family_attached", 25_000, 9_000, 1.1, 0.85, 8.4, 6.6),
        ("CO-multifamily_2_4", 18_000, 7_500, 0.85, 0.70, 6.8, 5.7),
        ("CO-multifamily_5plus", 40_000, 6_200, 0.55, 0.48, 5.1, 4.5),
        ("CO-mobile_home", 12_000, 8_800, 1.4, 0.95, 11.2, 7.8),
        ("CO-small_office_proxy", 4_000, 22_000, 12.0, 9.5, 95.0, 78.0),
    ]
    df = pd.DataFrame(
        rows,
        columns=[
            "segment",
            "n_units",
            "cost_per_unit",
            "base_peak_kw",
            "upgrade_peak_kw",
            "base_mwh_year",
            "upgrade_mwh_year",
        ],
    )
    df.to_csv(path, index=False)
    print(f"[warn] Synthetic demo written to {path} — not NREL EULP. Download CO baseline+upgrade CSVs for scoring.")
    return df


def _electricity_kw(df: pd.DataFrame) -> pd.Series:
    tcol = next((c for c in df.columns if "time" in c.lower()), df.columns[0])
    df = df.copy()
    df[tcol] = pd.to_datetime(df[tcol], errors="coerce")
    ecols = [
        c
        for c in df.columns
        if "electricity" in c.lower() and ("total" in c.lower() or "energy" in c.lower() or "consumption" in c.lower())
    ]
    if not ecols:
        num = df.select_dtypes(include="number").columns
        ecols = [num[0]] if len(num) else []
    if not ecols:
        raise ValueError("No electricity column found; see data/README.md")
    kwh = df.set_index(tcol)[ecols[0]].astype(float)
    # 15-min kWh → kW; if already hourly-ish, /1 is closer — detect median step
    if len(kwh.index) > 2:
        step_h = pd.Series(kwh.index).diff().median()
        hours = step_h.total_seconds() / 3600 if pd.notna(step_h) else 0.25
        hours = hours if hours and hours > 0 else 0.25
    else:
        hours = 0.25
    return kwh / hours


def _segment_from_name(path: Path) -> str:
    return path.stem.replace("up00-", "").replace("up0-", "").replace("up01-", "").replace("up1-", "")


def perceive_from_eulp(baseline_dir: Path, upgrade_dir: Path) -> pd.DataFrame | None:
    """Pair baseline/upgrade CSVs by filename token; return segment table or None."""
    if not baseline_dir.exists() or not upgrade_dir.exists():
        return None
    base_files = {p.name: p for p in baseline_dir.glob("*.csv")}
    up_files = {p.name: p for p in upgrade_dir.glob("*.csv")}
    if not base_files or not up_files:
        return None

    rows: list[dict[str, Any]] = []
    for uname, upath in sorted(up_files.items()):
        # match by building-type suffix (strip upgrade prefixes)
        token = _segment_from_name(upath)
        bpath = None
        for bname, bp in base_files.items():
            if token in bname or _segment_from_name(bp) == token:
                bpath = bp
                break
        if bpath is None:
            continue
        bkw = _electricity_kw(pd.read_csv(bpath))
        ukw = _electricity_kw(pd.read_csv(upath))
        aligned = pd.concat([bkw, ukw], axis=1, join="inner")
        aligned.columns = ["base", "up"]
        if aligned.empty:
            continue
        peak_base = float(aligned["base"].max())
        peak_up = float(aligned["up"].max())
        # series is aggregate kW for the stock slice; treat as one "unit" stock
        mwh_base = float(aligned["base"].sum() * (aligned.index.to_series().diff().median().total_seconds() / 3600.0) / 1000.0)
        mwh_up = float(aligned["up"].sum() * (aligned.index.to_series().diff().median().total_seconds() / 3600.0) / 1000.0)
        rows.append(
            {
                "segment": token,
                "n_units": 1,
                "cost_per_unit": 1.0e7,  # placeholder $ for the whole aggregate slice — replace with $/unit * count
                "base_peak_kw": peak_base,
                "upgrade_peak_kw": peak_up,
                "base_mwh_year": mwh_base,
                "upgrade_mwh_year": mwh_up,
            }
        )
    if not rows:
        return None
    print(f"[info] Built {len(rows)} segments from EULP CSVs")
    return pd.DataFrame(rows)


def perceive(baseline_dir: Path, upgrade_dir: Path, demo_csv: Path) -> pd.DataFrame:
    real = perceive_from_eulp(baseline_dir, upgrade_dir)
    if real is not None and len(real) >= 2:
        return real
    if demo_csv.exists():
        print(f"[warn] No paired EULP CSVs; using {demo_csv}")
        return pd.read_csv(demo_csv)
    return _synthesize_segments(demo_csv)


def greedy_allocate(df: pd.DataFrame, budget: float, peak_weight: float) -> pd.Series:
    """Fund whole segments in bang-per-buck order until budget is exhausted (fractional last segment)."""
    peak_save = (df["base_peak_kw"] - df["upgrade_peak_kw"]) * df["n_units"]
    energy_save = (df["base_mwh_year"] - df["upgrade_mwh_year"]) * df["n_units"]
    cost = df["cost_per_unit"] * df["n_units"]
    bang = (peak_weight * peak_save + (1.0 - peak_weight) * energy_save) / np.clip(cost, 1.0, None)
    order = np.argsort(-bang.to_numpy())
    frac = pd.Series(0.0, index=df.index)
    remaining = budget
    for idx in order:
        c = float(cost.iloc[idx])
        if c <= remaining:
            frac.iloc[idx] = 1.0
            remaining -= c
        elif remaining > 0:
            frac.iloc[idx] = remaining / c
            remaining = 0.0
            break
    return frac


def evaluate(df: pd.DataFrame, frac: pd.Series, budget: float, peak_weight: float) -> dict[str, float]:
    peak_save = ((df["base_peak_kw"] - df["upgrade_peak_kw"]) * df["n_units"] * frac).sum()
    energy_save = ((df["base_mwh_year"] - df["upgrade_mwh_year"]) * df["n_units"] * frac).sum()
    spent = (df["cost_per_unit"] * df["n_units"] * frac).sum()
    obj = peak_weight * peak_save + (1.0 - peak_weight) * energy_save
    return {
        "peak_kw_saved": float(peak_save),
        "mwh_saved": float(energy_save),
        "spent_usd": float(spent),
        "budget_usd": float(budget),
        "budget_violation": float(max(0.0, spent - budget)),
        "objective": float(obj),
        "usd_per_kw": float(spent / peak_save) if peak_save > 1e-9 else float("inf"),
    }


def run_agent_loop(df: pd.DataFrame, budget: float, max_iters: int = 3) -> None:
    peak_weight = 0.7
    greedy0 = greedy_allocate(df, budget, peak_weight=0.0)  # energy-first
    base_metrics = evaluate(df, greedy0, budget, peak_weight)

    for i in range(1, max_iters + 1):
        frac = greedy_allocate(df, budget, peak_weight=peak_weight)
        metrics = evaluate(df, frac, budget, peak_weight)
        print(f"=== iteration {i} (peak_weight={peak_weight:.2f}) ===")
        print("funded_fractions:")
        print(pd.DataFrame({"segment": df["segment"], "frac": frac.round(3)}).to_string(index=False))
        print("metrics:", {k: round(v, 2) if np.isfinite(v) else v for k, v in metrics.items()})
        print("energy_first_objective:", round(base_metrics["objective"], 2))
        if metrics["peak_kw_saved"] < base_metrics["peak_kw_saved"] * 0.9:
            peak_weight = min(0.95, peak_weight + 0.1)
            print("[revise] peak savings weak vs energy-first — raising peak weight")
        else:
            peak_weight = max(0.4, peak_weight - 0.05)
            print("[revise] peak OK — slightly more energy weight")
    print("TODO: integer dwelling counts; feeder peak cap; NREL package $ from documentation.")


def main() -> None:
    parser = argparse.ArgumentParser(description="Case 7 building-stock retrofit allocation starter agent")
    root = Path(__file__).parent
    parser.add_argument(
        "--baseline-dir",
        type=Path,
        default=root / "data" / "raw" / "nrel-eulp" / "baseline",
    )
    parser.add_argument(
        "--upgrade-dir",
        type=Path,
        default=root / "data" / "raw" / "nrel-eulp" / "upgrade",
    )
    parser.add_argument(
        "--demo-csv",
        type=Path,
        default=root / "data" / "raw" / "nrel-eulp" / "demo_segments.csv",
    )
    parser.add_argument("--budget", type=float, default=4.0e8, help="Program budget in USD")
    parser.add_argument("--iters", type=int, default=3)
    args = parser.parse_args()

    df = perceive(args.baseline_dir, args.upgrade_dir, args.demo_csv)
    run_agent_loop(df, budget=args.budget, max_iters=args.iters)


if __name__ == "__main__":
    main()
