#!/usr/bin/env python3
"""
IEEE YP Industry Hackathon — Stream 1 Starter Agent
Case: Autonomous Storage-Dispatch Agent for Building PV + Battery
Event: IEEE YP Industry Hackathon, Oct 2-4 2026, InceptionU Calgary

Minimal perceive -> reason -> act -> evaluate loop for behind-the-meter battery dispatch.
Replace TODOs with forecast models, optimization, and learned policies.
"""

from __future__ import annotations

import argparse
from dataclasses import dataclass
from pathlib import Path
from typing import Any

import numpy as np
import pandas as pd


@dataclass
class BuildingObservation:
    timestamps: pd.DatetimeIndex
    consumption_kw: np.ndarray
    production_kw: np.ndarray
    buy_price: np.ndarray
    sell_price: np.ndarray

    @property
    def net_load_kw(self) -> np.ndarray:
        return self.consumption_kw - self.production_kw


@dataclass
class DispatchAction:
    charge_kw: np.ndarray
    discharge_kw: np.ndarray
    notes: str


@dataclass
class BatteryParams:
    capacity_kwh: float = 50.0
    max_charge_kw: float = 25.0
    max_discharge_kw: float = 25.0
    charge_eff: float = 0.95
    discharge_eff: float = 0.95
    soc_min: float = 0.10
    soc_max: float = 0.90


def _synthesize_demo_csv(path: Path, periods: int = 96) -> None:
    """Write a 24-hour 15-min demo series when no real Power Laws CSV is present."""
    path.parent.mkdir(parents=True, exist_ok=True)
    rng = np.random.default_rng(42)
    t = pd.date_range("2019-06-01", periods=periods, freq="15min")
    hour = np.array([ts.hour + ts.minute / 60 for ts in t])
    consumption = 30 + 15 * np.sin((hour - 8) * np.pi / 12) + rng.normal(0, 2, periods)
    consumption = np.clip(consumption, 5, None)
    production = np.clip(40 * np.sin(np.pi * (hour - 6) / 12), 0, None)
    production = np.where((hour < 6) | (hour > 20), 0, production)
    buy_price = 0.08 + 0.06 * np.sin((hour - 17) * np.pi / 8)
    sell_price = buy_price * 0.6
    demo = pd.DataFrame(
        {
            "timestamp": t,
            "consumption": consumption,
            "production": production,
            "buy_price": buy_price,
            "sell_price": sell_price,
        }
    )
    demo.to_csv(path, index=False)
    print(f"[warn] Wrote synthetic 15-min demo CSV to {path}")
    print("[warn] This is NOT real Power Laws data. Replace with downloaded site CSVs per data/README.md.")


def perceive(site_csv: Path) -> BuildingObservation:
    """Load local Power Laws site CSV. See data/README.md for download instructions."""
    if not site_csv.exists():
        _synthesize_demo_csv(site_csv)

    df = pd.read_csv(site_csv)
    # Normalize column names
    col_map = {c.lower(): c for c in df.columns}
    time_col = col_map.get("timestamp", df.columns[0])
    cons_col = col_map.get("consumption", "consumption")
    prod_col = col_map.get("production", "production")
    buy_col = col_map.get("buy_price", "buy_price")
    sell_col = col_map.get("sell_price", "sell_price")

    for name, key in [
        ("consumption", cons_col),
        ("production", prod_col),
        ("buy_price", buy_col),
        ("sell_price", sell_col),
    ]:
        if key not in df.columns:
            # Fallback: first numeric columns after time
            nums = df.select_dtypes(include="number").columns
            idx = ["consumption", "production", "buy_price", "sell_price"].index(name)
            if idx < len(nums):
                df[name] = df[nums[idx]]
            else:
                df[name] = 0.0

    df[time_col] = pd.to_datetime(df[time_col])
    df = df.sort_values(time_col)

    return BuildingObservation(
        timestamps=pd.DatetimeIndex(df[time_col]),
        consumption_kw=df[cons_col if cons_col in df.columns else "consumption"].to_numpy(dtype=float),
        production_kw=df[prod_col if prod_col in df.columns else "production"].to_numpy(dtype=float),
        buy_price=df[buy_col if buy_col in df.columns else "buy_price"].to_numpy(dtype=float),
        sell_price=df[sell_col if sell_col in df.columns else "sell_price"].to_numpy(dtype=float),
    )


def reason(obs: BuildingObservation) -> dict[str, Any]:
    """Assess price spread and net-load statistics for dispatch planning."""
    spread = obs.buy_price - obs.sell_price
    return {
        "mean_net_load_kw": float(np.nanmean(obs.net_load_kw)),
        "peak_net_load_kw": float(np.nanmax(obs.net_load_kw)),
        "mean_buy_price": float(np.nanmean(obs.buy_price)),
        "mean_price_spread": float(np.nanmean(spread)),
        "pv_capacity_factor": float(np.nanmean(obs.production_kw) / (np.nanmax(obs.production_kw) + 1e-9)),
    }


def simulate_soc(
    obs: BuildingObservation,
    charge_kw: np.ndarray,
    discharge_kw: np.ndarray,
    battery: BatteryParams,
) -> np.ndarray:
    """Forward Euler SOC simulation over 15-min intervals (0.25 h)."""
    dt_h = 0.25
    soc = np.zeros(len(obs.timestamps) + 1)
    soc[0] = 0.5
    for i in range(len(obs.timestamps)):
        energy_in = charge_kw[i] * battery.charge_eff * dt_h
        energy_out = discharge_kw[i] / battery.discharge_eff * dt_h
        next_soc = soc[i] + (energy_in - energy_out) / battery.capacity_kwh
        soc[i + 1] = np.clip(next_soc, battery.soc_min, battery.soc_max)
    return soc[1:]


def act(
    obs: BuildingObservation,
    plan: dict[str, Any],
    battery: BatteryParams,
    charge_fraction: float = 0.5,
) -> DispatchAction:
    """
    Naive SOC policy: charge from PV surplus; discharge when buy price is high.
    TODO: replace with scipy.optimize / MILP / learned policy.
    """
    surplus = obs.production_kw - obs.consumption_kw
    price_rank = obs.buy_price / (np.nanmax(obs.buy_price) + 1e-9)

    charge = np.clip(surplus, 0, None) * charge_fraction
    charge = np.clip(charge, 0, battery.max_charge_kw)

    discharge = np.where(price_rank > 0.7, obs.consumption_kw * 0.3, 0.0)
    discharge = np.clip(discharge, 0, battery.max_discharge_kw)

    note = (
        f"naive SOC policy | charge_frac={charge_fraction:.2f} | "
        f"mean_buy=${plan['mean_buy_price']:.4f}/kWh"
    )
    return DispatchAction(charge_kw=charge, discharge_kw=discharge, notes=note)


def evaluate(
    obs: BuildingObservation,
    action: DispatchAction,
    battery: BatteryParams,
) -> dict[str, float]:
    """Compute electricity cost and constraint metrics."""
    dt_h = 0.25
    grid_import = obs.consumption_kw - obs.production_kw + action.charge_kw - action.discharge_kw
    grid_export = np.clip(-grid_import, 0, None)
    grid_import = np.clip(grid_import, 0, None)

    cost = np.nansum(grid_import * obs.buy_price * dt_h) - np.nansum(grid_export * obs.sell_price * dt_h)
    no_battery_import = np.clip(obs.consumption_kw - obs.production_kw, 0, None)
    baseline_cost = np.nansum(no_battery_import * obs.buy_price * dt_h)

    soc = simulate_soc(obs, action.charge_kw, action.discharge_kw, battery)
    soc_violations = int(np.sum((soc < battery.soc_min - 1e-6) | (soc > battery.soc_max + 1e-6)))

    return {
        "electricity_cost_usd": float(cost),
        "baseline_cost_usd": float(baseline_cost),
        "cost_savings_usd": float(baseline_cost - cost),
        "peak_grid_import_kw": float(np.nanmax(grid_import)),
        "total_charge_kwh": float(np.nansum(action.charge_kw) * dt_h),
        "total_discharge_kwh": float(np.nansum(action.discharge_kw) * dt_h),
        "final_soc": float(soc[-1]),
        "soc_violations": float(soc_violations),
    }


def run_agent_loop(
    obs: BuildingObservation,
    battery: BatteryParams,
    max_iters: int = 3,
) -> None:
    charge_fraction = 0.5
    best = None
    for i in range(1, max_iters + 1):
        plan = reason(obs)
        action = act(obs, plan, battery, charge_fraction=charge_fraction)
        metrics = evaluate(obs, action, battery)
        print(f"=== iteration {i} ===")
        print("plan:", plan)
        print("action:", action.notes)
        print("metrics:", metrics)
        best = metrics
        # Revise charge fraction based on cost savings signal (simple autonomy loop)
        if metrics["cost_savings_usd"] < 0:
            charge_fraction = max(0.2, charge_fraction - 0.1)
        else:
            charge_fraction = min(0.9, charge_fraction + 0.05)
        print(f"[revise] next charge_fraction={charge_fraction:.2f}")
    print("final:", best)


def main() -> None:
    parser = argparse.ArgumentParser(description="Case 2 building PV+battery dispatch starter agent")
    parser.add_argument(
        "--site-csv",
        type=Path,
        default=Path(__file__).parent / "data" / "raw" / "power-laws" / "demo_site_001.csv",
        help="Path to Power Laws site CSV (15-min load/PV/price)",
    )
    parser.add_argument("--capacity-kwh", type=float, default=50.0, help="Battery energy capacity (kWh)")
    parser.add_argument("--iters", type=int, default=3, help="Agent loop iterations")
    args = parser.parse_args()

    obs = perceive(args.site_csv)
    battery = BatteryParams(capacity_kwh=args.capacity_kwh)
    run_agent_loop(obs, battery, max_iters=args.iters)


if __name__ == "__main__":
    main()
