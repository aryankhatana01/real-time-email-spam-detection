import sys
sys.path.append('../')

from utils import create_producer
from ingestion.get_unread_emails import getEmails
import json
import datetime
import config
import time
from _logging import logger

# logger = get_logger()

producer = create_producer()

def create_record(id_, data):
    record = {}
    record['id'] = str(id_)
    record['subject'] = str(data['subject'])
    record['sender'] = str(data['sender'])
    record['body'] = str(data['body'])
    return record

if producer is not None:
    while True:
        emails = getEmails('2023/08/01')
        for id_, data in emails.items():
            record = create_record(id_, data)
            record['timestamp'] = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            producer.produce(topic=config.EMAILS_TOPIC, 
                          value=json.dumps(record).encode('utf-8'))
            logger.info(f"Sent email with id {id_} to Kafka")
            producer.flush()
            time.sleep(0.1) # Just a precaution
        time.sleep(30) # So that we don't get rate limited by the fuckin Gmail API
