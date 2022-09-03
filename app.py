import pickle
import os.path
from google.auth.transport.requests import Request
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from google.oauth2.credentials import Credentials
import email
import base64

# If modifying these scopes, delete the file token.json.
SCOPES = ['https://www.googleapis.com/auth/gmail.readonly']


def get_message(service, user_id, msg_id):

    try:
        message_list = service.users().messages().list(userId=user_id, id=msg_id, format='raw').execute()

        msg_raw = base64.urlsafe_b64decode(message['raw'].encode('ASCII'))


    except (errors.HttpError, error):
        print("An Error has happened, panic! Erorr:") % error:




def search_messages(service, user_id, search_string):
    
    try:
        search_id = service.users().messages().list(userId=user_id, q=search_string).execute()

        number_results = search_id['resultSizeEstimate']

        final_list = []
        if number_results > 0:
            message_ids = search_id['messages']

            for ids in message_ids:
                final_list.append(ids['id'])

        


        else:
            print('There were 0 results for that search string, returning an empty string')






    
    except (errors.HttpError, error):
        print("An Error has happened, panic! Erorr:") % error:


def get_service():

    creds = None
    # The file token.json stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.json', 'w') as token:
            token.write(creds.to_json())

    service = build('gmail', 'v1', credentials=creds)

    return service