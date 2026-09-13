"""Teen vs adult: keyword baseline -> style score -> blend activity once."""
from pathlib import Path

import numpy as np
import pandas as pd

JOINED = Path(__file__).parent / "data" / "teen_adult_joined.csv"


def prf(y_true: np.ndarray, y_pred: np.ndarray) -> tuple[float, float, float, float]:
    """precision, recall, false-teen rate, missed-teen rate."""
    y_true = y_true.astype(int)
    y_pred = y_pred.astype(int)
    tp = int(((y_pred == 1) & (y_true == 1)).sum())
    fp = int(((y_pred == 1) & (y_true == 0)).sum())
    fn = int(((y_pred == 0) & (y_true == 1)).sum())
    tn = int(((y_pred == 0) & (y_true == 0)).sum())
    prec = tp / (tp + fp) if (tp + fp) else 0.0
    rec = tp / (tp + fn) if (tp + fn) else 0.0
    false_teen = fp / (fp + tn) if (fp + tn) else 0.0  # adults wrongly called teen
    missed_teen = fn / (fn + tp) if (fn + tp) else 0.0
    return prec, rec, false_teen, missed_teen


def report(name: str, y_true: np.ndarray, y_pred: np.ndarray) -> None:
    prec, rec, ft, mt = prf(y_true, y_pred)
    acc = float((y_true == y_pred).mean())
    print(
        f"{name:28} acc={acc:.3f}  prec={prec:.3f}  rec={rec:.3f}  "
        f"false_teen={ft:.3f}  missed_teen={mt:.3f}"
    )


def main() -> None:
    df = pd.read_csv(JOINED)
    y = df["label_teen"].to_numpy()

    # --- Baseline: school/birthday keyword flag from posts ---
    baseline = df["keyword_teen_flag"].to_numpy()
    report("Baseline keywords", y, baseline)

    # --- v1: writing-style score (no activity yet) ---
    # Teens in this corpus tend toward shorter words, more first-person, more bangs/slang.
    style = (
        0.35 * (df["avg_word_len"] < 4.4).astype(float)
        + 0.25 * (df["first_person_rate"] > 0.06).astype(float)
        + 0.20 * (df["exclaim_rate"] > 0.008).astype(float)
        + 0.15 * (df["slang_emoji_rate"] > 0.002).astype(float)
        + 0.20 * (df["school_token_rate"] > 0).astype(float)
    )
    v1 = (style >= 0.55).astype(int).to_numpy()
    report("v1 style score>=0.55", y, v1)

    # --- Revise: blend style with Meta-like activity soft signals ---
    # Higher evening / short-video / night opens, lower school-hour activity -> more teen-like.
    activity = (
        0.25 * (df["pct_active_school_hours"] < 0.25).astype(float)
        + 0.25 * (df["pct_active_evening"] > 0.35).astype(float)
        + 0.20 * (df["share_short_video_views"] > 0.40).astype(float)
        + 0.15 * (df["night_notification_open_rate"] > 0.22).astype(float)
        + 0.15 * (df["weekend_weekday_session_ratio"] > 1.2).astype(float)
    )
    blend_w = 0.45  # weight on activity; change this and re-run
    blended = (1.0 - blend_w) * style + blend_w * activity
    v2 = (blended >= 0.50).astype(int).to_numpy()
    report(f"Revise blend w={blend_w}", y, v2)

    flipped = int((v1 != v2).sum())
    print(f"\nAccounts that flipped v1->revise: {flipped}/{len(df)}")
    print("Next: raise blend_w toward activity, or train LogisticRegression on the numeric columns.")
    print("Honesty: posts are 2004 blogs; activity columns are synthetic_calibrated_demo.")


if __name__ == "__main__":
    main()
