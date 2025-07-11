from services.sheets_service import read_sheet
from services.reminder_service import build_reminder_message_html
from services.email_service import send_reminders_to_all
from utils.secrets import get_gmail_password, get_gmail_sender, get_spreadsheet_id, get_spreadsheet_range, get_recipients

SPREADSHEET_ID = get_spreadsheet_id()
RANGE = get_spreadsheet_range()
EMAIL_RECIPIENTS = get_recipients()
SENDER_EMAIL = get_gmail_sender()
SENDER_PASSWORD = get_gmail_password()


def main():
    try:
        sheet_data = read_sheet(spreadsheet_id=SPREADSHEET_ID, range_name=RANGE)
    except Exception as e:
        print(f"Failed to return sheet data: {e}")
        return
    
    try:
        html_message = build_reminder_message_html(sheet_data)
    except Exception as e:
        print(f"Failed to build html reminder message: {e}")
        return
    
    if not html_message:
        print("No payments due in 2 days. Exiting.")
        return
    
    html_message, pay_date = html_message

    subject = f"💰 Upcoming Payment on {pay_date}"

    send_reminders_to_all(
        html_message=html_message,
        subject=subject,
        sender_email=SENDER_EMAIL,
        sender_password=SENDER_PASSWORD
    )


if __name__ == "__main__":
    main()
