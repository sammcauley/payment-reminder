from services.sheets_service import read_sheet
from services.reminder_service import build_reminder_message_html
from services.email_service import send_reminders_to_all
from utils.secrets import get_gmail_password, get_gmail_sender, get_spreadsheet_id, get_spreadsheet_range
from flask import Flask, jsonify

app = Flask(__name__)

@app.route("/", methods=["GET"])
def run_reminder():
    try:
        SPREADSHEET_ID = get_spreadsheet_id()
        RANGE = get_spreadsheet_range()
        SENDER_EMAIL = get_gmail_sender()
        SENDER_PASSWORD = get_gmail_password()

        sheet_data = read_sheet(spreadsheet_id=SPREADSHEET_ID, range_name=RANGE)
        html_result = build_reminder_message_html

        if not html_result:
            return jsonify({"status": "No payments due"}), 200

        html_message, pay_date = html_message
        subject = f"💰 Upcoming Payment on {pay_date}"

        send_reminders_to_all(
            html_message=html_message,
            subject=subject,
            sender_email=SENDER_EMAIL,
            sender_password=SENDER_PASSWORD
        )

        return jsonify({"status": "Emails sent successfully"}), 200
    
    except Exception as e:
        print(f"Error occurred: {e}")
        return jsonify({"error": str(e)}), 500
