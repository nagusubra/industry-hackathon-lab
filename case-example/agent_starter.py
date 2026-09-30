#!/usr/bin/env python3
"""
Case 6 starter: Is this text message a scam?

Pipeline (each function = one box in the system diagram in CASE.md):
    load -> extract_text_features -> keyword baseline
         -> text_score -> activity_score -> blend -> decide -> evaluate

Try:
    python agent_starter.py                          # defaults below
    python agent_starter.py --weight 0.6             # lean more on sender behaviour
    python agent_starter.py --cutoff 0.8             # stricter/looser blocking
    python agent_starter.py --logreg                 # optional stretch
"""
import argparse
import re
from pathlib import Path

import numpy as np
import pandas as pd

# ---- the two knobs you are allowed to turn ---------------------------------
ACTIVITY_WEIGHT = 0.0   # 0 = text only, 1 = behaviour only
CUTOFF = 1.0            # block if blended z-score >= CUTOFF
# ----------------------------------------------------------------------------

DATA = Path(__file__).parent / "data" / "sms_scam_joined.csv"

# Columns the model may NOT use (see "Rules" in CASE.md)
FORBIDDEN = {"label_scam", "message_family", "message_id"}

KEYWORDS = r"\b(?:free|win|winner|won|prize|claim|cash|urgent|gift card)\b"
URGENCY = r"\b(?:urgent|now|immediately|within|today|tonight|expire|suspended|verify|final|locked|midnight)\b"
URL = r"(?:https?://|www\.|\b[\w-]+\.(?:com|ca|top|info|xyz|ly|link|net|example)/\S*)"
CURRENCY = r"(?:\$\s?\d|\bdollars?\b)"
OPT_OUT = r"(?:reply stop|txt stop|stop to (?:opt|end|unsub))"
SECOND_PERSON = r"\b(?:you|your|you're|yours)\b"


# 1. Feature extraction (stateless, cheap: runs on every message) -----------
def extract_text_features(text: pd.Series) -> pd.DataFrame:
    t = text.fillna("")
    low = t.str.lower()
    words = low.str.split()
    n_words = words.str.len().clip(lower=1)
    letters = t.str.count(r"[A-Za-z]").clip(lower=1)
    return pd.DataFrame({
        "char_len": t.str.len(),
        "word_count": n_words,
        "avg_word_len": t.str.replace(r"\s+", "", regex=True).str.len() / n_words,
        "digit_ratio": t.str.count(r"\d") / t.str.len().clip(lower=1),
        "upper_ratio": t.str.count(r"[A-Z]") / letters,
        "has_url": low.str.contains(URL, regex=True).astype(int),
        "has_currency": low.str.contains(CURRENCY, regex=True).astype(int),
        "urgency_count": low.str.count(URGENCY),
        "exclaim_count": t.str.count("!"),
        "second_person_rate": low.str.count(SECOND_PERSON) / n_words,
        "has_opt_out": low.str.contains(OPT_OUT, regex=True).astype(int),
        "keyword_scam_flag": low.str.contains(KEYWORDS, regex=True).astype(int),
    }, index=text.index)


def z(s: pd.Series) -> pd.Series:
    sd = s.std()
    return (s - s.mean()) / (sd if sd > 0 else 1.0)


# 2. Scores -------------------------------------------------------------------
def text_score(f: pd.DataFrame) -> pd.Series:
    """Hand-weighted 'stylometry' score. Higher = more scam-like wording."""
    raw = (1.5 * f.has_url
           + 1.0 * f.has_currency
           + 0.8 * f.urgency_count
           + 3.0 * f.upper_ratio
           + 4.0 * f.digit_ratio
           + 3.0 * f.second_person_rate
           + 0.3 * f.exclaim_count
           - 1.5 * f.has_opt_out)       # real businesses must offer STOP
    return z(raw)


def activity_score(df: pd.DataFrame) -> pd.Series:
    """Sender-behaviour score. Higher = more scam-like sender."""
    raw = (2.0 * z(-np.log1p(df.sender_account_age_days))     # new sender
           + 1.0 * z(np.log1p(df.msgs_sent_last_hour))         # blasting
           + 1.0 * z(df.pct_recipients_not_in_contacts)        # texting strangers
           + 1.0 * z(-df.reply_rate_7d))                       # nobody writes back
    return z(raw)


# 3. Decision + evaluation ----------------------------------------------------
def evaluate(y_true, y_pred, name):
    y_true, y_pred = np.asarray(y_true), np.asarray(y_pred)
    tp = int(((y_pred == 1) & (y_true == 1)).sum())
    fp = int(((y_pred == 1) & (y_true == 0)).sum())
    fn = int(((y_pred == 0) & (y_true == 1)).sum())
    tn = int(((y_pred == 0) & (y_true == 0)).sum())
    precision = tp / (tp + fp) if tp + fp else 0.0
    recall = tp / (tp + fn) if tp + fn else 0.0
    false_block = fp / (fp + tn) if fp + tn else 0.0
    missed = fn / (tp + fn) if tp + fn else 0.0
    print(f"{name:<34} precision {precision:5.1%}  recall {recall:5.1%}  "
          f"false-block {false_block:5.1%}  missed-scam {missed:5.1%}  "
          f"(TP {tp}, FP {fp}, FN {fn}, TN {tn})")
    return dict(precision=precision, recall=recall, false_block=false_block, missed=missed)


def breakdown(df, pred, title):
    print(f"\n  {title} — flag rate by message family (scams want high, legit wants low):")
    tab = (pd.DataFrame({"family": df.message_family, "scam": df.label_scam, "flag": pred})
           .groupby(["scam", "family"]).flag.agg(["mean", "size"]))
    for (scam, fam), row in tab.iterrows():
        tag = "SCAM " if scam else "legit"
        print(f"    {tag} {fam:<22} flagged {row['mean']:5.1%}  (n={int(row['size'])})")


def run_logreg(df, feats):
    try:
        from sklearn.linear_model import LogisticRegression
        from sklearn.model_selection import train_test_split
        from sklearn.preprocessing import StandardScaler
        from sklearn.pipeline import make_pipeline
    except ImportError:
        print("\n[stretch] scikit-learn not installed: pip install scikit-learn")
        return
    X = pd.concat([feats.drop(columns=["keyword_scam_flag"]),
                   df[["sender_account_age_days", "msgs_sent_last_hour", "unique_recipients_24h",
                       "pct_recipients_not_in_contacts", "reply_rate_7d", "sent_hour"]]
                   .assign(sender_account_age_days=lambda d: np.log1p(d.sender_account_age_days),
                           msgs_sent_last_hour=lambda d: np.log1p(d.msgs_sent_last_hour),
                           unique_recipients_24h=lambda d: np.log1p(d.unique_recipients_24h))], axis=1)
    assert not FORBIDDEN & set(X.columns), "leakage: forbidden column in features"
    y = df.label_scam
    Xtr, Xte, ytr, yte = train_test_split(X, y, test_size=0.3, stratify=y, random_state=0)
    model = make_pipeline(StandardScaler(), LogisticRegression(max_iter=1000, class_weight="balanced"))
    model.fit(Xtr, ytr)
    proba = model.predict_proba(Xte)[:, 1]
    print("\n[stretch] Logistic regression on a 30% held-out split:")
    for thr in (0.5, 0.8, 0.95):
        evaluate(yte, (proba >= thr).astype(int), f"  logreg p>={thr}")
    coefs = pd.Series(model[-1].coef_[0], index=X.columns).sort_values(key=abs, ascending=False)
    print("  top weights (standardised):", ", ".join(f"{k} {v:+.2f}" for k, v in coefs.head(6).items()))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--weight", type=float, default=ACTIVITY_WEIGHT, help="activity blend weight 0..1")
    ap.add_argument("--cutoff", type=float, default=CUTOFF, help="block if blended z >= cutoff")
    ap.add_argument("--logreg", action="store_true", help="optional stretch model")
    ap.add_argument("--breakdown", action="store_true", help="show flag rate per message family")
    args = ap.parse_args()

    df = pd.read_csv(DATA)
    feats = extract_text_features(df.text)
    y = df.label_scam

    print(f"Loaded {len(df)} messages, {y.mean():.1%} scams.  weight={args.weight}  cutoff={args.cutoff}\n")

    base = feats.keyword_scam_flag
    evaluate(y, base, "Baseline: keyword rule")

    ts = text_score(feats)
    evaluate(y, (ts >= args.cutoff).astype(int), "Text-style score only")

    acts = activity_score(df)
    evaluate(y, (acts >= args.cutoff).astype(int), "Sender-activity score only")

    blended = z((1 - args.weight) * ts + args.weight * acts)
    pred = (blended >= args.cutoff).astype(int)
    evaluate(y, pred, f"Blend (w={args.weight}, cut={args.cutoff})")

    if args.breakdown:
        breakdown(df, base, "Baseline")
        breakdown(df, pred, "Blend")

    if args.logreg:
        run_logreg(df, feats)


if __name__ == "__main__":
    main()
