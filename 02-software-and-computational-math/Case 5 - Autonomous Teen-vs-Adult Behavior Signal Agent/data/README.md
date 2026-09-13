# Data Guide — Teen vs Adult Behavior Signals (Case 5)

You are practicing Meta-style **age assurance from soft signals**: writing style + app activity. No typed birthday. No camera / face data.

---

## Bundled hour-one files (in this folder)

| File | Rows (approx.) | What it is |
|---|---|---|
| `teen_adult_joined.csv` | 3,000 accounts | **Start here.** One row per user: text features + activity features + `label_teen` |
| `blogger_posts_sample.csv` | ~9,000 posts | Real blog posts (truncated) from the Blog Authorship Corpus with age labels |
| `blogger_user_features.csv` | 3,000 | Text-only aggregates (stylometry + keyword flag) |
| `blogger_activity_synthetic.csv` | ~5,500 | Calibrated synthetic activity table (linked users + extras) |
| `blogger_hourly_sessions_sample.csv` | subset | Synthetic hourly session counts for a smaller user set |

### Labels

- `is_teen` / `label_teen` = 1 if age is **13–17**, else 0 (ages **23+** in this pack).
- The Blog Authorship Corpus intentionally has almost no 18–22 authors; we keep that gap so the binary task stays clean.

---

## Where the data comes from

### Real text (Blog Authorship Corpus, 2004)

- Source: Schler, Koppel, Argamon & Pennebaker (2006), *Effects of Age and Gender on Blogging*.
- Hugging Face mirror: [barilan/blog_authorship_corpus](https://huggingface.co/datasets/barilan/blog_authorship_corpus) (`data/blogs.zip`).
- Self-reported ages on Blogger.com. Bands in the original corpus: 13–17, 23–27, 33–47.
- These are **real people writing real posts**, not Meta/Instagram/TikTok private data. Treat them as a public writing-style proxy.

### Synthetic activity (practice logs)

Platforms do **not** publish private login/engagement logs tied to verified age. The activity columns are a **calibrated demo** (`source = synthetic_calibrated_demo`) shaped like signals Meta and journalists describe:

- quieter during school hours for many teens
- more evening / weekend sessions
- higher short-video share
- higher night notification opens

They are **not** extracted from Facebook, Instagram, TikTok, or YouTube. About 12% of synthetic users deliberately follow the *other* band’s pattern (homeschooled teens, night-shift adults, etc.) so the task is not trivial.

---

## Suggested features

**Text:** `avg_word_len`, `first_person_rate`, `school_token_rate`, `birthday_token_rate`, `exclaim_rate`, `slang_emoji_rate`, `keyword_teen_flag`

**Activity:** `pct_active_school_hours`, `pct_active_evening`, `pct_active_late_night`, `weekend_weekday_session_ratio`, `sessions_per_day`, `avg_session_minutes`, `share_short_video_views`, `share_news_views`, `night_notification_open_rate`

Do **not** train on `age` itself if you are pretending the birthday is missing or lying — use `label_teen` only as the answer key for scoring.

---

## Larger optional download

Hour-one work does **not** require an external download — `teen_adult_joined.csv` is enough.

If you want the fuller activity table (~10k users) and the longer hourly session log, download the official Case 5 pack:

- **GitHub Release (no login):** https://github.com/nagusubra/industry-hackathon-lab/releases/download/case5-teen-adult-data/ieee-yp-hackathon-2026-case5-teen-adult.zip
- **Kaggle (hackathon dataset page):** *organizers will paste the URL here after the Kaggle dataset is published*

You can also pull more raw blogs from Hugging Face if you want a bigger text set:

```python
from huggingface_hub import hf_hub_download
path = hf_hub_download(
    repo_id="barilan/blog_authorship_corpus",
    repo_type="dataset",
    filename="data/blogs.zip",
)
```

---

## Loading example

```python
import pandas as pd

df = pd.read_csv("data/teen_adult_joined.csv")
print(df["label_teen"].value_counts())
print(df[["avg_word_len", "pct_active_evening", "label_teen"]].head())
```

---

## License / citation

- Blog text: Blog Authorship Corpus — cite Schler et al. (2006); respect the corpus’s research-use norms.
- Synthetic activity: generated for this hackathon lab (MIT with the rest of the repo). Do not present it as Meta production telemetry.
