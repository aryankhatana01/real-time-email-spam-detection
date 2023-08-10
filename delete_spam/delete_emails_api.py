from googleapiclient.discovery import build
from google.auth.transport.requests import Request
from google_auth_oauthlib.flow import InstalledAppFlow
import os
from google.oauth2.credentials import Credentials

def move_email_to_trash(email_id):
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
        # Modify the labels of the email to move it to the trash
        modify_labels = {'removeLabelIds': ['INBOX'], 'addLabelIds': ['TRASH']}
        service.users().messages().modify(userId='me', id=email_id, body=modify_labels).execute()
        print(f"Email with ID {email_id} moved to trash successfully.")
    except Exception as e:
        print(f"An error occurred while moving the email to trash: {e}")

if __name__ == "__main__":
    email_id_to_move = "189da250851508b9"
    move_email_to_trash(email_id_to_move)
