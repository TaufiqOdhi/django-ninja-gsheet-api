from __future__ import print_function

import os.path
from drf_gsheet_api.settings import BASE_DIR

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

# If modifying these scopes, delete the file token.json.
SCOPES = [
    'https://www.googleapis.com/auth/spreadsheets.readonly',
    'https://www.googleapis.com/auth/spreadsheets'
]

SPREADSHEET_ID = '1FMPomLzI_iUUINCal3EwYz3NZkF4HYBgA64RQfPbTo8'
TOKEN_LOCATION = os.path.join(BASE_DIR, 'token.json')


def login_auth():
    flow = InstalledAppFlow.from_client_secrets_file(
        os.path.join(BASE_DIR, 'credentials.json'), SCOPES)
    creds = flow.run_local_server(port=0).to_json()
    # Save the credentials for the next run
    with open(TOKEN_LOCATION, 'w') as token:
        token.write(creds)
    return creds


def auth_google_api():
    """Shows basic usage of the Sheets API.
    Prints values from a sample spreadsheet.
    """
    creds = None
    # The file token.json stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists(TOKEN_LOCATION):
        creds = Credentials.from_authorized_user_file(TOKEN_LOCATION, SCOPES)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            login_auth()
    try:
        service = build('sheets', 'v4', credentials=creds)
        return service
    except HttpError as err:
        print(err)
        return None
