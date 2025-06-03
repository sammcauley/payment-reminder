import pytest
import builtins
import json
from unittest.mock import patch, mock_open, MagicMock
from services import email_service

def test_load_email_recipients_success():
    mock_data = '{"Alice": "alice@example.com"}'
    with patch("builtins.open", mock_open(read_data=mock_data)):
        result = email_service.load_email_recipients("dummy.json")
        assert result == {"Alice": "alice@example.com"}

def test_load_email_recipients_file_error():
    with patch("builtins.open", side_effect=FileNotFoundError):
        result = email_service.load_email_recipients("missing.json")
        assert result == {}

@patch("smtplib.SMTP")
def test_send_email_success(mock_smtp):
    mock_server = MagicMock()
    mock_smtp.return_value.__enter__.return_value = mock_server

    result = email_service.send_email(
        subject="Test",
        html_content="<p>Hello</p>",
        recipient_email="test@example.com",
        sender_email="sender@gmail.com",
        sender_password="password123"
    )

    assert result is True
    mock_server.starttls.assert_called_once()
    mock_server.login.assert_called_once_with("sender@gmail.com", "password123")
    mock_server.sendmail.assert_called_once()

@patch("smtplib.SMTP", side_effect=Exception("SMTP Error"))
def test_send_email_failure(mock_smtp):
    result = email_service.send_email(
        subject="Fail",
        html_content="<p>Error</p>",
        recipient_email="test@example.com",
        sender_email="sender@gmail.com",
        sender_password="badpass"
    )
    assert result is False

@patch("services.email_service.send_email", return_value=True)
@patch("services.email_service.load_email_recipients")
def test_send_reminders_to_all_all_success(mock_load, mock_send):
    mock_load.return_value = {
    "Alice": "alice@valid.com",
    "Bob": "bob@valid.com"
}
    email_service.send_reminders_to_all(
        html_message="<p>Reminder</p>",
        subject="Pay Reminder",
        json_path="emails.json",
        sender_email="test@gmail.com",
        sender_password="pass"
    )
    assert mock_send.call_count == 2

@patch("services.email_service.load_email_recipients")
@patch("services.email_service.send_email", return_value=False)
def test_send_reminders_to_all_all_fail(mock_load, mock_send):
    mock_load.return_value = {"Alice": "alice@example.com"}
    email_service.send_reminders_to_all(
        html_message="<p>Reminder</p>",
        subject="Pay Reminder",
        json_path="emails.json",
        sender_email="test@gmail.com",
        sender_password="pass"
    )
    assert mock_send.call_count == 1