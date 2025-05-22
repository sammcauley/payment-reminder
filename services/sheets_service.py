from google.oauth2 import service_account
from googleapiclient.discovery import build
from pathlib import Path
from typing import List
import os
from dotenv import load_dotenv

load_dotenv()

SCOPES = ['https://www.googleapis.com/auth/spreadsheets.readonly']

BASE_DIR = Path(__file__).parent.parent
SERVICE_ACCOUNT_FILE = BASE_DIR / "terraform" / "sheets-key.json"

RANGE = "Bookings!A1:P"
SPREADSHEET_ID = os.getenv("SPREADSHEET_ID")
if not SPREADSHEET_ID:
    raise ValueError("Missing SPREADHSEET_ID in environment variables.")

credentials = service_account.Credentials.from_service_account_file(
    SERVICE_ACCOUNT_FILE, scopes=SCOPES
)

service = build('sheets', 'v4', credentials=credentials)

def read_sheet(spreadsheet_id: str = SPREADSHEET_ID, range_name: str = RANGE) -> List[List[str]]:
    try:
        sheet = service.spreadsheets()
        result = sheet.values().get(spreadsheetId=spreadsheet_id,
                                    range=range_name).execute()
        return result.get('values', [])
    except Exception as e:
        print(f"Error reading sheet: {e}")
        return []
    

if __name__ == "__main__":
    data = read_sheet()
    for row in data:
        print(row)