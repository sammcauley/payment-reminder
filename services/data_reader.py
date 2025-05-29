import pandas as pd
from typing import List

def parse_sheet_data(data: List[List[str]]) -> pd.DataFrame:
    headers = [h.upper() for h in data[0]]
    rows = data[1:]
    df = pd.DataFrame(rows, columns=headers)

    for date_col in ["PAY DATE", "START DATE", "END DATE"]:
        if date_col in df.columns:
            df[date_col] = pd.to_datetime(df[date_col], format="%d/%m/%y", errors="coerce")

    if "AMOUNT (GBP)" in df.columns:
        df["AMOUNT (GBP)"] = pd.to_numeric(df["AMOUNT (GBP)"], errors="coerce")

    return df