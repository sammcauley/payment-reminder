import pandas as pd

def safe_str(val):
    return str(val).strip() if pd.notna(val) else ""