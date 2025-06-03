import pandas as pd
from datetime import datetime, timedelta
from typing import List, Optional
from services.data_reader import parse_sheet_data
from utils.strings import safe_str

def filter_due_reminders(df: pd.DataFrame) -> pd.DataFrame:
    today = datetime.today().date()

    df = df.copy()
    df["PAY DATE"] = pd.to_datetime(df["PAY DATE"], errors="coerce")

    df = df[df["PAY DATE"].notna()]

    df["DAYS_UNTIL_PAY"] = (df["PAY DATE"] - pd.Timestamp(today)).dt.days

    return df[
        (df["TO PAY/ALREADY PAID"] == "To pay") &
        (df["DAYS_UNTIL_PAY"] == 2)
    ]

def build_reminder_row_html(row: pd.Series) -> Optional[str]:
    try:
        booking_type = safe_str(row.get("TYPE", ""))
        name = safe_str(row.get("NAME", ""))
        location = safe_str(row.get("CITY", ""))
        local_amount = safe_str(row.get("AMOUNT (LOCAL)", ""))
        gbp_amount = safe_str(row.get("AMOUNT (GBP)", ""))
        method = safe_str(row.get("METHOD", ""))
        card = safe_str(row.get("CARD", ""))

        description = f"{booking_type} {name}"
        if booking_type in {"Accommodation", "Car"} and location:
            description += f" in {location}"

        if not local_amount:
            amount = f"£{gbp_amount}"
        else:
            amount = f"{local_amount} (around £{gbp_amount})"

        if method.lower() == "card" and card:
            payment = f"from {card} 💳"
        elif method.lower() == "cash":
            payment = "in cash 💷"
        elif method:
            payment = f"{method.lower()} 💰"
        else:
            payment = ""

        return f"{description} - {amount} {payment}".strip(" -")

    except Exception:
        return None

def build_reminder_message_html(data) -> Optional[str]:
    df = parse_sheet_data(data)
    filtered_df = filter_due_reminders(df)

    if filtered_df.empty:
        return None

    pay_date_obj = filtered_df.iloc[0]["PAY DATE"]
    pay_date_str = pay_date_obj.strftime("%d/%m/%y")

    html_parts = [
        "🔔 Payment Reminder!",
        f"<p>You have the following payments due on <strong>{pay_date_str}</strong>:</p>",
        "<ul>"
    ]

    for _, row in filtered_df.iterrows():
        item = build_reminder_row_html(row)
        if item:
            html_parts.append(f"<li>{item}</li>")

    html_parts.extend([
        "</ul>",
        "<p><strong>Make sure you have enough money for the payments! 💱</p>"
    ])

    return " ".join(html_parts), pay_date_str
