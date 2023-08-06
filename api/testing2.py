import os
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.discovery import build

# Define the scopes needed for Gmail API
SCOPES = ['https://www.googleapis.com/auth/gmail.readonly']

def get_gmail_service():
    # Load or create credentials
    creds = None
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    # If credentials are not available or are expired, authenticate via OAuth2 flow
    if not creds or not creds.valid:
        flow = InstalledAppFlow.from_client_secrets_file('credentials.json', SCOPES)
        creds = flow.run_local_server(port=0)
        # Save the credentials for future use
        with open('token.json', 'w') as token:
            token.write(creds.to_json())

    # Build the Gmail API service
    service = build('gmail', 'v1', credentials=creds)
    return service

def list_messages(service, user_id='me', query=''):
    try:
        # List messages matching the query
        response = service.users().messages().list(userId=user_id, q=query).execute()
        messages = response.get('messages', [])
        return messages
    except Exception as e:
        print('An error occurred:', e)
        return []

def get_message(service, user_id='me', msg_id=''):
    try:
        # Get the content of a specific message
        message = service.users().messages().get(userId=user_id, id=msg_id).execute()
        return message
    except Exception as e:
        print('An error occurred:', e)
        return None

if __name__ == '__main__':
    # Get the Gmail API service
    gmail_service = get_gmail_service()

    # List the last 5 messages in your inbox
    messages = list_messages(gmail_service, query='in:inbox', user_id='me')
    i = 0
    for message in messages:
        msg = get_message(gmail_service, user_id='me', msg_id=message['id'])
        # print(f"Subject: {msg['subject']}")
        # print(f"From: {msg['from']}")
        # print(f"Snippet: {msg['snippet']}")
        # print("-" * 50)
        print(msg)
        print("-" * 50)
        if i>5:
            break
        i += 1
