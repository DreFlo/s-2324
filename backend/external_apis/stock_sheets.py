from __future__ import print_function

import os.path
import csv

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

'''
Follow this tutorial to setup the google sheets environment
https://developers.google.com/sheets/api/quickstart/python

Save the credentials.json file in the external_apis folder

I added the credentials.json and the token.json (which will be create automatically later) to the .gitignore file
'''

# If modifying these scopes, delete the file token.json.
SCOPES = ['https://www.googleapis.com/auth/spreadsheets']

def main():
    creds = None
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
        
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                './backend/external_apis/credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.json', 'w') as token:
            token.write(creds.to_json())

    try:
        service = build('sheets', 'v4', credentials=creds)

        # Call the Sheets API
        _ = service.spreadsheets()
        
        spreadsheet = {
            'properties': {
                'title': 'stocks'
            }
        }
        spreadsheet = service.spreadsheets().create(body=spreadsheet,) \
            .execute()
        
        spreadsheetId = spreadsheet.get('spreadsheetId')
        
        #We need to find a good initial date for all of them
        body = {
            'values': [['=GOOGLEFINANCE("NASDAQ:GOOG", "price", DATE(2010,1,1), TODAY(), "DAILY")']]
        }
        
        _ = service.spreadsheets().values().update(
            spreadsheetId=spreadsheetId, range="A1:A1",
            valueInputOption="USER_ENTERED", body=body).execute()
        
        result = service.spreadsheets().values().get(
            spreadsheetId=spreadsheetId, range="Sheet1").execute()
        
        
        values = result.get('values', [])
        if not values:
            print('No data found.')
            return
        
        with open('stocks.csv', 'w', newline='') as csvfile:
            writer = csv.writer(csvfile, delimiter=',')
            writer.writerows(values)
        
    except HttpError as err:
        print(err)


if __name__ == '__main__':
    main()