from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
import json
import os
import logging


logging.basicConfig(
    format="%(asctime)s %(levelname)-8s %(message)s",
    level=logging.INFO,
    datefmt="%Y-%m-%d %H:%M:%S",
)


# If modifying these scopes, delete the file token.json.
SCOPES = ['https://www.googleapis.com/auth/spreadsheets']

# The ID and range of a sample spreadsheet.
SAMPLE_SPREADSHEET_ID = '1-gvqOJJVd7SxsSd4asqMujl0JXgdQj-f6_KAGLTtinE'
SAMPLE_RANGE_NAME = 'VaxBotV2'

def upload_to_sheets(row_data):
    # print("uploading this")
    # print(row_data)
    try:
        token = os.environ["SHEETS_TOKEN"]
        creds = Credentials.from_authorized_user_info(json.loads(token), SCOPES)
        creds.refresh(Request())
        service = build('sheets', 'v4', credentials=creds)
        values = row_data
        body = {'values': values}
        sheet = service.spreadsheets()
        result = sheet.values().append(spreadsheetId=SAMPLE_SPREADSHEET_ID,
                                    range=SAMPLE_RANGE_NAME, valueInputOption="RAW", body=body).execute()
        print(result)
    except Exception as e:
        logging.error(e)