import smtplib
import json
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.utils import parseaddr
from google.cloud import secretmanager
from utils.secrets import get_recipients

GMAIL_SMTP_SERVER = "smtp.gmail.com"
GMAIL_SMTP_PORT = 587
    
def send_email(subject: str, html_content: str, recipient_email: str, sender_email: str, sender_password: str) -> bool:
    try:
        message = MIMEMultipart("alternative")
        message["Subject"] = subject
        message["From"] = sender_email
        message["To"] = recipient_email

        plain_text = "This is a payment reminder. Please view the email in an HTML-compatible client."
        message.attach(MIMEText(plain_text, "plain"))
        message.attach(MIMEText(html_content, "html", "utf-8"))

        with smtplib.SMTP(GMAIL_SMTP_SERVER, GMAIL_SMTP_PORT) as server:
            server.starttls()
            server.login(sender_email, sender_password)
            server.sendmail(sender_email, recipient_email, message.as_string())

        print(f"✅ Email sent to {recipient_email}")
        return True
    except Exception as e:
        print(f"❌ Failed to send email to {recipient_email}: {e}")
        return False
    
def send_reminders_to_all(html_message: str, subject:str, sender_email: str, sender_password: str):
    recipients = get_recipients()
    if not recipients:
        print("❌ No recipients found.")
        return
    
    failed = []
    
    for name, email in recipients.items():
        _, addr = parseaddr(email)
        if "@" not in addr:
            print(f"❌ Invalid email address for {name}: {email}")
            continue

        print(f"Sending email reminder to {name} <{email}>...")
        success = send_email(subject, html_message, email, sender_email, sender_password)
        if not success:
            failed.append(email)

    if failed:
        print(f"❌ Failed to send reminders to {len(failed)} recipients: {', '.join(failed)}")
    else:
        print("✅ All reminders sent successfully.")