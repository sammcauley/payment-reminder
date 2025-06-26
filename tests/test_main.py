import pytest
from unittest.mock import patch, MagicMock
import sys
import os

# Add the root directory (payment-reminder/) to sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))


@patch("main.send_reminders_to_all")
@patch("main.build_reminder_message_html")
@patch("main.read_sheet")
def test_main_success(mock_read_sheet, mock_build_html, mock_send_reminders):
    mock_read_sheet.return_value = [["headers"], ["row1"], ["row2"]]
    mock_build_html.return_value = ("<p>Test reminder</p>", "28/06/25")

    from main import main
    main()

    mock_read_sheet.assert_called_once()
    mock_build_html.assert_called_once()
    mock_send_reminders.assert_called_once()


@patch("main.send_reminders_to_all")
@patch("main.build_reminder_message_html")
@patch("main.read_sheet")
def test_main_no_due_payments(mock_read_sheet, mock_build_html, mock_send_reminders):
    mock_read_sheet.return_value = [["headers"], ["row1"], ["row2"]]
    mock_build_html.return_value = None

    from main import main
    main()

    mock_read_sheet.assert_called_once()
    mock_build_html.assert_called_once()
    mock_send_reminders.assert_not_called()


@patch("main.send_reminders_to_all")
@patch("main.build_reminder_message_html", side_effect=Exception("Message build failed"))
@patch("main.read_sheet")
def test_main_build_failure(mock_read_sheet, mock_build_html, mock_send_reminders):
    mock_read_sheet.return_value = [["headers"], ["row1"], ["row2"]]

    from main import main
    main()

    mock_read_sheet.assert_called_once()
    mock_build_html.assert_called_once()
    mock_send_reminders.assert_not_called()


@patch("main.send_reminders_to_all")
@patch("main.build_reminder_message_html")
@patch("main.read_sheet", side_effect=Exception("Sheet read failed"))
def test_main_sheet_failure(mock_read_sheet, mock_build_html, mock_send_reminders):
    from main import main
    main()

    mock_read_sheet.assert_called_once()
    mock_build_html.assert_not_called()
    mock_send_reminders.assert_not_called()