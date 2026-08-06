#!/usr/bin/env python3
"""
IEEE YP Industry Hackathon — Stream 4 Starter Agent
Case: Autonomous Reaction-Condition Optimizer

Active-learning / bandit loop over a hidden HTE yield oracle.
Do NOT train on the full table — only observe yields for proposed conditions.
"""

from __future__ import annotations

import argparse
import json
from dataclasses import dataclass, field
from pathlib import Path

import numpy as np
import pandas as pd


LIGANDS = ["P(t-Bu)3", "XPhos", "SPhos", "RuPhos", "BrettPhos", "DavePhos", "P(o-tol)3"]
BASES = ["Cs2CO3", "K3PO4", "NaOtBu", "LiHMDS", "K2CO3"]
SOLVENTS = ["toluene", "dioxane", "THF", "DMF", "MeCN"]


def synthetic_hte_table(path: Path, n_rows: int = 200) -> pd.DataFrame:
    """Build a Buchwald-Hartwig-style yield table with hidden structure."""
    path.parent.mkdir(parents=True, exist_ok=True)
    rng = np.random.default_rng(7)
    rows = []
    for i in range(n_rows):
        lig = rng.choice(LIGANDS)
        base = rng.choice(BASES)
        solv = rng.choice(SOLVENTS)
        # Hidden yield landscape: synergistic combos score higher
        lig_bonus = {"BrettPhos": 18, "XPhos": 14, "SPhos": 12}.get(lig, 4)
        base_bonus = {"Cs2CO3": 12, "K3PO4": 10}.get(base, 3)
        solv_bonus = {"toluene": 8, "dioxane": 6}.get(solv, 2)
        noise = rng.normal(0, 6)
        yield_pct = float(np.clip(25 + lig_bonus + base_bonus + solv_bonus + noise, 0, 99))
        rows.append(
            {
                "condition_id": f"bh-{i:04d}",
                "ligand": lig,
                "base": base,
                "solvent": solv,
                "yield_pct": yield_pct,
            }
        )
    df = pd.DataFrame(rows)
    df.to_csv(path, index=False)
    print(f"[info] Wrote synthetic HTE table to {path}")
    return df


def load_or_synthesize(csv_path: Path) -> pd.DataFrame:
    if csv_path.exists():
        return pd.read_csv(csv_path)
    return synthetic_hte_table(csv_path)


@dataclass
class HiddenYieldOracle:
    """Yield oracle — reveals only queried condition IDs."""

    table: pd.DataFrame
    revealed: dict[str, float] = field(default_factory=dict)

    @property
    def optimum(self) -> float:
        col = "yield_pct" if "yield_pct" in self.table.columns else "yield"
        return float(self.table[col].max())

    def query(self, condition_id: str) -> float:
        if condition_id in self.revealed:
            return self.revealed[condition_id]
        row = self.table[self.table["condition_id"] == condition_id]
        if row.empty:
            raise KeyError(condition_id)
        col = "yield_pct" if "yield_pct" in row.columns else "yield"
        y = float(row.iloc[0][col])
        self.revealed[condition_id] = y
        return y

    def all_ids(self) -> list[str]:
        return self.table["condition_id"].astype(str).tolist()


@dataclass
class UCB1Bandit:
    """UCB1 over categorical condition arms."""

    arms: list[str]
    counts: dict[str, int] = field(default_factory=dict)
    rewards: dict[str, float] = field(default_factory=dict)
    total_pulls: int = 0

    def select(self, k: int, rng: np.random.Generator) -> list[str]:
        unseen = [a for a in self.arms if self.counts.get(a, 0) == 0]
        picks: list[str] = []
        if unseen:
            picks.extend(unseen[:k])
        while len(picks) < k:
            best_arm = None
            best_score = -np.inf
            for arm in self.arms:
                if arm in picks:
                    continue
                n = self.counts.get(arm, 0)
                if n == 0:
                    score = np.inf
                else:
                    mean = self.rewards[arm] / n
                    score = mean + np.sqrt(2 * np.log(max(self.total_pulls, 1)) / n)
                if score > best_score:
                    best_score = score
                    best_arm = arm
            if best_arm is None:
                break
            picks.append(best_arm)
        rng.shuffle(picks)
        return picks[:k]

    def update(self, arm: str, reward: float) -> None:
        self.counts[arm] = self.counts.get(arm, 0) + 1
        self.rewards[arm] = self.rewards.get(arm, 0.0) + reward
        self.total_pulls += 1


def random_baseline(oracle: HiddenYieldOracle, budget: int, rng: np.random.Generator) -> float:
    ids = rng.choice(oracle.all_ids(), size=min(budget, len(oracle.all_ids())), replace=False)
    best = 0.0
    for cid in ids:
        best = max(best, oracle.query(str(cid)))
    return best


def run_bandit_loop(
    oracle: HiddenYieldOracle,
    budget: int,
    batch_size: int,
    seed: int,
    strategy: str = "ucb",
) -> dict:
    rng = np.random.default_rng(seed)
    arms = oracle.all_ids()
    bandit = UCB1Bandit(arms=arms)
    log: list[dict] = []
    best_yield = 0.0
    pulls = 0

    round_num = 0
    while pulls < budget:
        round_num += 1
        k = min(batch_size, budget - pulls)
        if strategy == "random":
            pool = [a for a in arms if a not in oracle.revealed]
            if not pool:
                break
            chosen = list(rng.choice(pool, size=min(k, len(pool)), replace=False))
        else:
            chosen = bandit.select(k, rng)

        batch_yields = []
        for cid in chosen:
            if pulls >= budget:
                break
            y = oracle.query(cid)
            bandit.update(cid, y)
            pulls += 1
            best_yield = max(best_yield, y)
            batch_yields.append(y)

        entry = {
            "round": round_num,
            "proposed": chosen,
            "yields": batch_yields,
            "best_so_far": best_yield,
            "budget_used": pulls,
        }
        log.append(entry)
        print(f"=== round {round_num} === best_yield={best_yield:.1f}%  budget={pulls}/{budget}")
        print(f"  proposed: {chosen}")
        print(f"  observed: {[f'{y:.1f}' for y in batch_yields]}")

    regret = oracle.optimum - best_yield
    return {
        "best_yield": best_yield,
        "optimum": oracle.optimum,
        "regret": regret,
        "queries": len(oracle.revealed),
        "log": log,
    }


def main() -> None:
    parser = argparse.ArgumentParser(description="Stream 4 reaction-condition optimizer starter agent")
    parser.add_argument(
        "--csv",
        type=Path,
        default=Path(__file__).parent / "data" / "raw" / "hte_buchwald.csv",
    )
    parser.add_argument("--budget", type=int, default=20, help="Max oracle queries (wet-lab experiments)")
    parser.add_argument("--batch-size", type=int, default=4, help="Conditions per round")
    parser.add_argument("--seed", type=int, default=42)
    parser.add_argument("--strategy", choices=["ucb", "random"], default="ucb")
    parser.add_argument("--out", type=Path, default=Path(__file__).parent / "data" / "raw" / "query_log.json")
    args = parser.parse_args()

    table = load_or_synthesize(args.csv)
    oracle = HiddenYieldOracle(table=table)

    print(f"[info] Hidden oracle ready: {len(table)} conditions, optimum={oracle.optimum:.1f}%")
    print(f"[info] Strategy={args.strategy}, budget={args.budget}, batch_size={args.batch_size}")
    print("[warn] Do NOT fit a model on the full table — only use queried yields.\n")

    result = run_bandit_loop(
        oracle,
        budget=args.budget,
        batch_size=args.batch_size,
        seed=args.seed,
        strategy=args.strategy,
    )

    rng = np.random.default_rng(args.seed + 1)
    # Fresh oracle for fair baseline comparison
    baseline_oracle = HiddenYieldOracle(table=table)
    rand_best = random_baseline(baseline_oracle, args.budget, rng)
    print(f"\n[baseline] random search best_yield={rand_best:.1f}%  regret={oracle.optimum - rand_best:.1f}")
    print(f"[agent]    {args.strategy} best_yield={result['best_yield']:.1f}%  regret={result['regret']:.1f}")

    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text(json.dumps(result, indent=2))
    print(f"[info] Query log saved to {args.out}")
    print("TODO: swap synthetic oracle for Iron Mind / rxn_yields HTE tables.")


if __name__ == "__main__":
    main()
