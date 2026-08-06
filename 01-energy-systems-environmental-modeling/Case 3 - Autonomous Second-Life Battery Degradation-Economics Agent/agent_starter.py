#!/usr/bin/env python3
"""
IEEE YP Industry Hackathon — Stream 1 Starter Agent
Case: Autonomous Second-Life Battery Degradation-Economics Agent
Event: IEEE YP Industry Hackathon, Oct 2-4 2026, InceptionU Calgary

Minimal perceive -> reason -> act -> evaluate loop for second-life battery
cycling economics vs. capacity fade. Replace TODOs with real SOH models and policies.
"""

from __future__ import annotations

import argparse
from dataclasses import dataclass
from pathlib import Path
from typing import Any

import numpy as np
import pandas as pd


@dataclass
class CellObservation:
    cycle_numbers: np.ndarray
    capacity_ah: np.ndarray
    soh: np.ndarray
    duty_cycle_label: str


@dataclass
class CyclingPolicy:
    depth_of_discharge: float
    cycles_per_year: float
    notes: str


@dataclass
class EconomicsParams:
    revenue_per_kwh: float = 0.15
    replacement_cost_usd: float = 5000.0
    discount_rate: float = 0.08
    retirement_soh: float = 0.70
    nominal_capacity_kwh: float = 5.0


def _synthesize_fade_curves(path: Path, n_cycles: int = 500) -> None:
    """Write synthetic capacity-fade curves when no OSF data is present."""
    path.parent.mkdir(parents=True, exist_ok=True)
    rng = np.random.default_rng(7)
    cycles = np.arange(1, n_cycles + 1)
    # Empirical fade: faster early fade, residential vs commercial duty
    for label, fade_rate in [("residential", 0.0008), ("commercial", 0.0012)]:
        fade = 1.0 - fade_rate * cycles - 0.00002 * cycles ** 1.3
        fade = np.clip(fade, 0.65, 1.0) + rng.normal(0, 0.002, n_cycles)
        capacity_ah = fade * 5.0  # 5 Ah nominal INR21700-class
        df = pd.DataFrame(
            {
                "cycle_number": cycles,
                "capacity_ah": capacity_ah,
                "soh": fade,
                "duty_cycle": label,
            }
        )
        out = path / f"synthetic_{label}_fade.csv"
        df.to_csv(out, index=False)
        print(f"[info] Wrote synthetic fade curve to {out}")


def _pick_csv(csv_files: list[Path], duty_cycle: str | None) -> Path:
    """Select a CSV deterministically; prefer residential duty-cycle files."""
    if duty_cycle:
        needle = duty_cycle.lower()
        matches = [p for p in csv_files if needle in p.name.lower() or needle in str(p).lower()]
        if matches:
            return sorted(matches)[0]
    residential = [p for p in csv_files if "residential" in p.name.lower() or "residential" in str(p).lower()]
    if residential:
        return sorted(residential)[0]
    return sorted(csv_files)[0]


def perceive(data_dir: Path, duty_cycle: str | None = None) -> CellObservation:
    """Load OSF second-life cycling data or synthetic fade CSVs."""
    data_dir.mkdir(parents=True, exist_ok=True)

    csv_files = sorted(data_dir.rglob("*.csv"))
    if not csv_files:
        _synthesize_fade_curves(data_dir)
        csv_files = sorted(data_dir.rglob("*.csv"))

    chosen = _pick_csv(csv_files, duty_cycle)
    print(f"[info] Loading {chosen}")
    df = pd.read_csv(chosen)
    col_lower = {c.lower(): c for c in df.columns}

    cycle_col = col_lower.get("cycle_number", col_lower.get("cycle", df.columns[0]))
    cap_col = col_lower.get("capacity_ah", col_lower.get("capacity", None))
    soh_col = col_lower.get("soh", col_lower.get("capacity_retention", None))

    cycles = df[cycle_col].to_numpy(dtype=float)
    if cap_col and cap_col in df.columns:
        capacity = df[cap_col].to_numpy(dtype=float)
        soh = capacity / (capacity[0] + 1e-9)
    elif soh_col and soh_col in df.columns:
        soh = df[soh_col].to_numpy(dtype=float)
        capacity = soh * 5.0
    else:
        nums = df.select_dtypes(include="number")
        capacity = nums.iloc[:, -1].to_numpy(dtype=float)
        soh = capacity / (capacity[0] + 1e-9)

    duty = "unknown"
    if "duty_cycle" in col_lower:
        duty = str(df[col_lower["duty_cycle"]].iloc[0])

    return CellObservation(
        cycle_numbers=cycles,
        capacity_ah=capacity,
        soh=soh,
        duty_cycle_label=duty,
    )


def reason(obs: CellObservation) -> dict[str, Any]:
    """Estimate fade rate and remaining useful life from observed SOH curve."""
    n = len(obs.soh)
    if n < 2:
        fade_per_cycle = 0.001
    else:
        fade_per_cycle = float((obs.soh[0] - obs.soh[-1]) / (obs.cycle_numbers[-1] - obs.cycle_numbers[0] + 1))

    return {
        "initial_soh": float(obs.soh[0]),
        "final_soh_observed": float(obs.soh[-1]),
        "fade_per_cycle": fade_per_cycle,
        "cycles_observed": int(n),
        "duty_cycle": obs.duty_cycle_label,
    }


def act(plan: dict[str, Any], depth_of_discharge: float, cycles_per_year: float) -> CyclingPolicy:
    """
    Propose cycling depth and annual cycle count.
    TODO: replace with optimization over fade model + price signals.
    """
    note = (
        f"cycle policy | DOD={depth_of_discharge:.0%} | "
        f"cycles/yr={cycles_per_year:.0f} | fade/cycle={plan['fade_per_cycle']:.5f}"
    )
    return CyclingPolicy(
        depth_of_discharge=depth_of_discharge,
        cycles_per_year=cycles_per_year,
        notes=note,
    )


def evaluate(
    plan: dict[str, Any],
    policy: CyclingPolicy,
    econ: EconomicsParams,
    horizon_years: float = 5.0,
) -> dict[str, float]:
    """Simulate lifecycle revenue vs. fade cost to retirement SOH."""
    fade_per_cycle = plan["fade_per_cycle"]
    # Deeper cycling accelerates fade (square-law stress proxy)
    effective_fade = fade_per_cycle * (policy.depth_of_discharge ** 2) / 0.25

    total_cycles = policy.cycles_per_year * horizon_years
    projected_soh = plan["initial_soh"] - effective_fade * total_cycles
    projected_soh = max(projected_soh, 0.5)

    energy_per_cycle_kwh = policy.depth_of_discharge * econ.nominal_capacity_kwh
    annual_revenue = policy.cycles_per_year * energy_per_cycle_kwh * econ.revenue_per_kwh
    total_revenue = annual_revenue * horizon_years

    replacement_needed = projected_soh < econ.retirement_soh
    replacement_cost = econ.replacement_cost_usd if replacement_needed else 0.0
    npv_revenue = total_revenue / (1 + econ.discount_rate) ** (horizon_years / 2)
    lifecycle_value = npv_revenue - replacement_cost

    return {
        "projected_soh": float(projected_soh),
        "total_cycles": float(total_cycles),
        "effective_fade_per_cycle": float(effective_fade),
        "annual_revenue_usd": float(annual_revenue),
        "replacement_needed": float(1.0 if replacement_needed else 0.0),
        "lifecycle_npv_usd": float(lifecycle_value),
    }


def run_agent_loop(
    obs: CellObservation,
    econ: EconomicsParams,
    max_iters: int = 3,
) -> None:
    depth_of_discharge = 0.80
    cycles_per_year = 300.0
    best = None
    for i in range(1, max_iters + 1):
        plan = reason(obs)
        policy = act(plan, depth_of_discharge, cycles_per_year)
        metrics = evaluate(plan, policy, econ)
        print(f"=== iteration {i} ===")
        print("plan:", plan)
        print("policy:", policy.notes)
        print("metrics:", metrics)
        best = metrics
        # Revise: if retirement triggered, reduce DOD; else cautiously increase revenue
        if metrics["replacement_needed"] > 0:
            depth_of_discharge = max(0.40, depth_of_discharge - 0.10)
            cycles_per_year = max(100.0, cycles_per_year - 50.0)
        else:
            depth_of_discharge = min(0.95, depth_of_discharge + 0.05)
        print(f"[revise] next DOD={depth_of_discharge:.0%}, cycles/yr={cycles_per_year:.0f}")
    print("final:", best)


def main() -> None:
    parser = argparse.ArgumentParser(description="Case 3 second-life battery economics starter agent")
    parser.add_argument(
        "--data-dir",
        type=Path,
        default=Path(__file__).parent / "data" / "raw" / "second-life",
        help="Directory with OSF unzip or synthetic fade CSVs",
    )
    parser.add_argument("--iters", type=int, default=3, help="Agent loop iterations")
    parser.add_argument(
        "--duty-cycle",
        type=str,
        default=None,
        help="Prefer CSV matching duty cycle (e.g. residential, commercial)",
    )
    args = parser.parse_args()

    obs = perceive(args.data_dir, duty_cycle=args.duty_cycle)
    econ = EconomicsParams()
    run_agent_loop(obs, econ, max_iters=args.iters)


if __name__ == "__main__":
    main()
