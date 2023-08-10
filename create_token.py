import os.path
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request

SCOPES = [
    'https://www.googleapis.com/auth/gmail.readonly', 
    'https://www.googleapis.com/auth/gmail.modify', 
]

def get_gmail_service():
    # Load or create credentials
    creds = None
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json')
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

def copy_token_file():
    # Copy token.json to the computation folder
    import shutil
    # shutil.copyfile('token.json', 'computation/token.json')
    shutil.copyfile('token.json', 'delete_spam/token.json')
    shutil.copyfile('token.json', 'ingestion/token.json')

if __name__ == "__main__":
    get_gmail_service()
    copy_token_file()