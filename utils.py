# src/utils.py
import pandas as pd
from pathlib import Path
from .preprocess import load_and_clean
from .data_generator import generate_synthetic_poll

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data"
CLEAN = DATA / "cleaned_poll.csv"
RAW = DATA / "synthetic_poll.csv"

def load_cleaned():
    """
    Load the cleaned CSV from disk. Raises FileNotFoundError if missing.
    """
    if not CLEAN.exists():
        raise FileNotFoundError(f"Cleaned CSV not found at {CLEAN}")
    return pd.read_csv(CLEAN, parse_dates=["Date"], dayfirst=False, encoding="utf-8-sig", low_memory=False)

def save_cleaned_from_df(df: pd.DataFrame):
    """
    Save a DataFrame to the cleaned CSV path (overwrites).
    """
    DATA.mkdir(parents=True, exist_ok=True)
    df.to_csv(CLEAN, index=False, encoding="utf-8")
    return CLEAN

def ensure_clean_exists(generate_if_missing=False, n_rows=500):
    """
    Ensure the cleaned CSV exists. If not present and generate_if_missing True,
    generate synthetic raw data and run preprocess to produce it.
    """
    if CLEAN.exists():
        return CLEAN
    if generate_if_missing:
        # create raw synthetic and then clean it
        generate_synthetic_poll(n_rows=n_rows, out_path=RAW)
        # run the module's load_and_clean to produce CLEAN
        df = load_and_clean(path=RAW)
        save_cleaned_from_df(df)
        return CLEAN
    raise FileNotFoundError("Cleaned CSV missing. Run src/data_generator.py and src/preprocess.py or use generate_if_missing=True.")

# small utility for ad-hoc cleaning of an uploaded DataFrame before using in app
def prep_uploaded_df(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()
    # standardize column names (strip)
    df.columns = [c.strip() if isinstance(c,str) else c for c in df.columns]
    # try timestamp handling
    if "Timestamp" in df.columns and "Date" not in df.columns:
        df["Timestamp"] = pd.to_datetime(df["Timestamp"], errors="coerce")
        df["Date"] = df["Timestamp"].dt.date
    # ensure Satisfaction numeric
    if "Satisfaction (1-5)" in df.columns:
        df["Satisfaction (1-5)"] = pd.to_numeric(df["Satisfaction (1-5)"], errors="coerce")
    # trim text fields
    for c in ["Preferred Tool", "Feedback", "Age Group", "Gender"]:
        if c in df.columns:
            df[c] = df[c].astype(str).str.strip()
    return df
