from google.cloud import secretmanager
import json
from typing import Optional, Union

def get_secret(name: str) -> Optional[Union[dict, str]]:
    try:
        client = secretmanager.SecretManagerServiceClient()
        secret_name = f"projects/995259718626/secrets/{name}/versions/latest"
        response = client.access_secret_version(request={"name": secret_name})
        payload = response.payload.data.decode("UTF-8")
        try:
            return json.loads(payload)
        except json.JSONDecodeError:
            return payload
    except Exception as e:
        print(f"Error loading secret '{name}': {e}")
        return None
    

def get_gmail_sender() -> str:
    gmail_sender = get_secret("Gmail-sender-address")
    if not isinstance(gmail_sender, str):
        raise ValueError("Gmail Sender Address must be stored as a plain string.")
    return gmail_sender

def get_gmail_password() -> str:
    gmail_password = get_secret("Gmail-app-password")
    if not isinstance(gmail_password, str):
        raise ValueError("Gmail App Password must be stored as a plain string.")
    return gmail_password

def get_spreadsheet_range() -> str:
    spreadsheet_range = get_secret("spreadsheet-range")
    if not isinstance(spreadsheet_range, str):
        raise ValueError("Spreadsheet Range must be stored as a plain string.")
    return spreadsheet_range

def get_spreadsheet_id() -> str:
    spreadsheet_id = get_secret("spreadsheet-test-id")
    if not isinstance(spreadsheet_id, str):
        raise ValueError("Spreadsheet ID must be stored as a plain string.")
    return spreadsheet_id

def get_recipients() -> dict:
    recipients = get_secret("receiver-emails")
    if not isinstance(recipients, dict):
        raise ValueError("Email Recipients must be stored as JSON.")
    return recipients