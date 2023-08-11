from googleapiclient.discovery import build
from google.auth.transport.requests import Request
from google_auth_oauthlib.flow import InstalledAppFlow
import os
from google.oauth2.credentials import Credentials

def mark_email_as_unread(email_id):
    # If modifying these scopes, delete the token.json file.
    SCOPES = ['https://www.googleapis.com/auth/gmail.modify']

    # Set up the Gmail API credentials
    creds = None
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        with open('token.json', 'w') as token:
            token.write(creds.to_json())

    # Create the Gmail API service
    service = build('gmail', 'v1', credentials=creds)

    try:
        # Modify the labels of the email to mark it as unread
        modify_labels = {'addLabelIds': ['UNREAD']}
        service.users().messages().modify(userId='me', id=email_id, body=modify_labels).execute()
        print(f"Email with ID {email_id} marked as unread successfully.")
    except Exception as e:
        print(f"An error occurred while marking the email as unread: {e}")

if __name__ == "__main__":
    email_id_to_mark = "test"
    mark_email_as_unread(email_id_to_mark)