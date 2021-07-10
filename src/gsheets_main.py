from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
import json
import os

# If modifying these scopes, delete the file token.json.
SCOPES = ['https://www.googleapis.com/auth/spreadsheets']

# The ID and range of a sample spreadsheet.
SAMPLE_SPREADSHEET_ID = '1-gvqOJJVd7SxsSd4asqMujl0JXgdQj-f6_KAGLTtinE'
SAMPLE_RANGE_NAME = 'VaxBot'

def upload_to_sheets(row_data):
    # print("uploading this")
    # print(row_data)
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

