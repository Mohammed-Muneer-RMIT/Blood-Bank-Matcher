import pandas as pd
from pathlib import Path

def load_csv_default(path, default_df):
    p = Path(path)
    if p.exists():
        return pd.read_csv(p)
    return default_df.copy()

def ensure_types(df):
    # Basic cleaning hooks if needed
    return df
