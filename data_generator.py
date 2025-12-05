# src/data_generator.py
import random
import numpy as np
import pandas as pd
from datetime import datetime, timedelta
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "data"
OUT.mkdir(parents=True, exist_ok=True)

def generate_synthetic_poll(n_rows=500, out_path=OUT / "synthetic_poll.csv", seed=42):
    random.seed(seed)
    np.random.seed(seed)
    start = datetime(2024,1,1)
    rows = []
    age_groups = ["18-24","25-34","35-44","45-54","55+"]
    genders = ["Male","Female","Other","Prefer not to say"]
    tools = ["Python","R","Excel","Tableau","Other"]
    for i in range(n_rows):
        ts = start + timedelta(days=random.randint(0, 365), hours=random.randint(0,23))
        age = random.choice(age_groups)
        gender = random.choice(genders)
        pref = random.choices(tools, weights=[0.4,0.15,0.25,0.15,0.05])[0]
        satisfaction = random.choices([1,2,3,4,5], weights=[0.05,0.1,0.25,0.35,0.25])[0]
        # text feedback: some positive, neutral, negative templates
        if satisfaction >= 4:
            feedback = random.choice([
                "Great tool, easy to use",
                "Loved it — very helpful",
                "Would recommend to friends"
            ])
        elif satisfaction == 3:
            feedback = random.choice([
                "It's okay, some features missing",
                "Neutral experience",
                "Could be improved"
            ])
        else:
            feedback = random.choice([
                "Not satisfied, many issues",
                "Hard to use and slow",
                "Needs major improvements"
            ])
        rows.append({
            "Timestamp": ts.strftime("%Y-%m-%d %H:%M:%S"),
            "Age Group": age,
            "Gender": gender,
            "Preferred Tool": pref,
            "Satisfaction (1-5)": satisfaction,
            "Feedback": feedback
        })
    df = pd.DataFrame(rows)
    df.to_csv(out_path, index=False, encoding="utf-8")
    print(f"Synthetic poll saved to: {out_path}")
    return df

if __name__ == "__main__":
    generate_synthetic_poll(800)
