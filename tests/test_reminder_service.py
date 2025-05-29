import pytest
from datetime import datetime, timedelta
import pandas as pd
from services.reminder_service import filter_due_reminders, build_reminder_row_html, build_reminder_message_html
from services.data_reader import parse_sheet_data

# === Mock Data ===

def sample_sheet_data_with_due_and_non_due():
    today = datetime.today().date()
    due_date = today + timedelta(days=2)

    return [
        ["TYPE", "NAME", "CITY", "PAY DATE", "TO PAY/ALREADY PAID", "AMOUNT (LOCAL)", "AMOUNT (GBP)", "METHOD", "CARD"],
        ["Hotel", "Marriott", "London", due_date.strftime("%d/%m/%y"), "To pay", "", "250", "Card", "Monzo"],
        ["Flight", "British Airways", "", "01/01/25", "Already paid", "", "120", "Card", "Amex"],
        ["Car", "Hertz", "Madrid", due_date.strftime("%d/%m/%y"), "To pay", " EUR 100", "85", "Cash", ""],
    ]

def sheet_data_no_due():
    return [
        ["TYPE", "NAME", "CITY", "PAY DATE", "TO PAY/ALREADY PAID", "AMOUNT (LOCAL)", "AMOUNT (GBP)", "METHOD", "CARD"],
        ["Hotel", "Hilton", "Berlin", "01/01/25", "Already paid", "", "180", "Card", "Visa"]
    ]

def malformed_data():
    return [
        ["TYPE", "NAME", "CITY", "PAY DATE", "TO PAY/ALREADY PAID", "AMOUNT (LOCAL)", "AMOUNT (GBP)", "METHOD", "CARD"],
        ["", "", "", "not a date", "To pay", "", "", "", ""]
    ]


# === Tests ===

def test_filter_due_reminders_returns_only_due():
    data = sample_sheet_data_with_due_and_non_due()
    df = parse_sheet_data(data)
    filtered = filter_due_reminders(df)

    assert not filtered.empty
    assert len(filtered) == 2
    assert all(filtered["TO PAY/ALREADY PAID"] == "To pay")
    assert all((filtered["PAY DATE"].dt.date - datetime.today().date()) == timedelta(days=2))


def test_filter_due_reminders_returns_empty_if_none_due():
    data = sheet_data_no_due()
    df = parse_sheet_data(data)
    filtered = filter_due_reminders(df)

    assert filtered.empty


def test_build_reminder_message_html_generates_valid_output():
    data = sample_sheet_data_with_due_and_non_due()
    message = build_reminder_message_html(data)

    assert message is not None
    assert "<ul>" in message
    assert "Marriott" in message
    assert " EUR 100" in message
    assert "Monzo" in message
    assert "Make sure you have enough money" in message


def test_build_reminder_message_returns_none_if_no_due():
    data = sheet_data_no_due()
    message = build_reminder_message_html(data)

    assert message is None


def test_graceful_handling_of_malformed_data():
    data = malformed_data()
    df = parse_sheet_data(data)
    filtered = filter_due_reminders(df)

    # Shouldn't throw and should return empty
    assert filtered.empty

    message = build_reminder_message_html(data)
    assert message is None