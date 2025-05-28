import pandas as pd
from typing import List

def parse_sheet_data(data: List[List[str]]) -> pd.DataFrame:
    headers = [h.upper() for h in data[0]]
    rows = data[1:]
    df = pd.DataFrame(rows, columns = headers)

    if "PAY DATE" in df.columns:
        df["PAY DATE"] = pd.to_datetime(df["PAY DATE"], format="%d/%m/%y", errors="coerce")
    if "START DATE" in df.columns:
        df["START DATE"] = pd.to_datetime(df["START DATE"], format="%d/%m/%y", errors="coerce")
    if "END DATE" in df.columns:
        df["END DATE"] = pd.to_datetime(df["END DATE"], format="%d/%m/%y", errors="coerce")
    if "AMOUNT (GBP)" in df.columns:
        df["AMOUNT (GBP)"] = pd.to_numeric(df["AMOUNT (GBP)"], errors="coerce")

    return df