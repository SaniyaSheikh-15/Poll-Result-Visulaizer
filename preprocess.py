# src/preprocess.py
import pandas as pd
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data"
RAW = DATA / "synthetic_poll.csv"
OUT = DATA / "cleaned_poll.csv"

def load_and_clean(path=RAW):
    # read robustly (utf-8-sig then fallback)
    try:
        df = pd.read_csv(path, encoding="utf-8-sig")
    except Exception:
        df = pd.read_csv(path, encoding="latin1")

    # standardize column names
    df.columns = [c.strip() if isinstance(c, str) else c for c in df.columns]

    # timestamp -> datetime
    if "Timestamp" in df.columns:
        df["Timestamp"] = pd.to_datetime(df["Timestamp"], errors="coerce")
        df["Date"] = df["Timestamp"].dt.date

    # trim text columns
    for c in ["Preferred Tool","Feedback","Age Group","Gender"]:
        if c in df.columns:
            df[c] = df[c].astype(str).str.strip()

    # satisfaction numeric
    if "Satisfaction (1-5)" in df.columns:
        df["Satisfaction (1-5)"] = pd.to_numeric(df["Satisfaction (1-5)"], errors="coerce").astype("Int64")

    # feedback length feature
    if "Feedback" in df.columns:
        df["Feedback Length"] = df["Feedback"].astype(str).apply(len)
    else:
        df["Feedback Length"] = 0

    # drop rows missing core fields
    required = []
    if "Preferred Tool" in df.columns:
        required.append("Preferred Tool")
    if "Satisfaction (1-5)" in df.columns:
        required.append("Satisfaction (1-5)")
    if required:
        df = df.dropna(subset=required)

    DATA.mkdir(parents=True, exist_ok=True)
    df.to_csv(OUT, index=False, encoding="utf-8")
    return df

if __name__ == "__main__":
    df = load_and_clean()
    print("Cleaned rows:", len(df))
    print("Saved:", OUT)
