import pandas as pd
from datetime import datetime, timedelta
from typing import List, Optional
from services.data_reader import parse_sheet_data
from utils.strings import safe_str

def filter_due_reminders(df: pd.DataFrame) -> pd.DataFrame:
    today = datetime.today().date()

    df = df[df["PAY DATE"].notna()]

    due_df = df[
        (df["TO PAY/ALREADY PAID"] == "To pay") &
        (df["PAY DATE"].apply(lambda d: d.date() - today == timedelta(days=2)))
    ]
    
    return due_df

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
            payment = f"from {card}"
        elif method.lower() == "cash":
            payment = "in cash"
        elif method:
            payment = f"via {method.lower()}"
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

    pay_date = filtered_df.iloc[0]["PAY DATE"].strftime("%d/%m/%y")

    # Start HTML message
    html_parts = [
        "<h2>Payment Reminder! <i class='fa-solid fa-bell'></i></h2>",
        f"<p>You have the following payments due on <strong>{pay_date}</strong>:</p>",
        "<ul>"
    ]

    for _, row in filtered_df.iterrows():
        item = build_reminder_row_html(row)
        if item:
            html_parts.append(f"<li>{item}</li>")

    html_parts.extend([
        "</ul>",
        "<p><strong>Make sure you have enough money for the payments!<i class='fa-solid fa-money-bill-wave'></i></strong></p>"
    ])

    return " ".join(html_parts)
