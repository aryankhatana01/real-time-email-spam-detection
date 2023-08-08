from googleapiclient.discovery import build
import os.path
import base64
from google.oauth2.credentials import Credentials
from bs4 import BeautifulSoup
from datetime import datetime
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request

SCOPES = ['https://www.googleapis.com/auth/gmail.readonly', 'https://www.googleapis.com/auth/gmail.modify']

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
                '../credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.json', 'w') as token:
            token.write(creds.to_json())

    # Build the Gmail API service
    service = build('gmail', 'v1', credentials=creds)
    return service


def getEmails(after_date):
    # Connect to the Gmail API
    service = get_gmail_service()
    after_datetime = datetime.strptime(after_date, '%Y/%m/%d')
    query = f"is:unread after:{after_datetime.strftime('%Y/%m/%d')}"

    # request a list of all the messages
    result = service.users().messages().list(userId='me', q=query).execute()

    # We can also pass maxResults to get any number of emails. Like this:
    # result = service.users().messages().list(maxResults=200, userId='me').execute()
    messages = result.get('messages')

    # messages is a list of dictionaries where each dictionary contains a message id.

    # iterate through all the messages
    emails_d = {}
    if messages is not None:
        for msg in messages:
            # Get the message from its id
            txt = service.users().messages().get(userId='me', id=msg['id']).execute()

            # Use try-except to avoid any Errors
            try:
                # Get value of 'payload' from dictionary 'txt'
                payload = txt['payload']
                headers = payload['headers']

                # Look for Subject and Sender Email in the headers
                for d in headers:
                    if d['name'] == 'Subject':
                        subject = d['value']
                    if d['name'] == 'From':
                        sender = d['value']

                # The Body of the message is in Encrypted format. So, we have to decode it.
                # Get the data and decode it with base 64 decoder.
                parts = payload.get('parts')[0]
                data = parts['body']['data']
                data = data.replace("-","+").replace("_","/")
                decoded_data = base64.b64decode(data)

                # Now, the data obtained is in lxml. So, we will parse 
                # it with BeautifulSoup library
                soup = BeautifulSoup(decoded_data , "lxml")
                body = soup.body()
                id_ = msg['id']

                # Printing the subject, sender's email and message
                print("Subject: ", subject)
                print("From: ", sender)
                print("Message: ", body)
                print('\n')
                emails_d[id_] = {'subject': subject, 'sender': sender, 'body': body}
                resp = service.users().messages().modify(userId='me', id=id_, body={'removeLabelIds': ['UNREAD']}).execute()
                print(resp)
            except Exception as e:
                pass
    return emails_d

if __name__ == "__main__":
    # This function gets all the UNREAD emails from the inbox after a certain date (01/08/2023) and marks them as READ
    emails_d = getEmails('2023/08/01')
    print(emails_d)