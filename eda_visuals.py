# src/eda_visuals.py
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from wordcloud import WordCloud
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "outputs" / "figures"
OUT.mkdir(parents=True, exist_ok=True)

def bar_preference(df, col="Preferred Tool", save_to=OUT/"bar_pref.png"):
    plt.figure(figsize=(8,4))
    order = df[col].value_counts().index
    sns.countplot(data=df, x=col, order=order)
    plt.xticks(rotation=30)
    plt.tight_layout()
    plt.savefig(save_to, dpi=150)
    plt.close()
    return save_to

def hist_satisfaction(df, col="Satisfaction (1-5)", save_to=OUT/"hist_sat.png"):
    plt.figure(figsize=(6,4))
    sns.histplot(df[col].dropna().astype(int), bins=5, kde=True)
    plt.tight_layout()
    plt.savefig(save_to, dpi=150)
    plt.close()
    return save_to

def line_responses_over_time(df, date_col="Date", save_to=OUT/"line_daily.png"):
    if date_col in df.columns:
        df[date_col] = pd.to_datetime(df[date_col], errors="coerce")
        daily = df.dropna(subset=[date_col]).groupby(df[date_col].dt.date).size()
    else:
        daily = pd.Series(dtype=int)
    plt.figure(figsize=(8,3))
    daily.plot(marker='o')
    plt.tight_layout()
    plt.savefig(save_to, dpi=150)
    plt.close()
    return save_to

def make_wordcloud(df, text_col="Feedback", save_to=OUT/"wordcloud.png"):
    text = " ".join(df[text_col].astype(str).tolist())
    if not text.strip():
        return None
    wc = WordCloud(width=800, height=400, background_color='white').generate(text)
    plt.figure(figsize=(10,5))
    plt.imshow(wc, interpolation='bilinear')
    plt.axis('off')
    plt.tight_layout()
    plt.savefig(save_to, dpi=150)
    plt.close()
    return save_to
