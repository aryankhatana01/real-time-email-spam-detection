# This files consumes from the predictions and deletes the spam emails using the gmail api
import sys
sys.path.append('../')

from utils import create_consumer
import json
import config
from _logging import logger
from delete_emails_api import move_email_to_trash

consumer = create_consumer(topic=config.PREDICTIONS_TOPIC, group_id=config.PREDICTIONS_GROUP_ID)

def delete_spam_emails():
    while True:
        message = consumer.poll()
        if message is None:
            # time.sleep(15)
            continue
        if message.error():
            logger.error("Consumer error: {}".format(message.error()))
            continue
        record = json.loads(message.value().decode('utf-8'))
        consumer.commit(message)
        if record['prediction'] == [1]: # Spam
            logger.info(f"Deleting email with id {record['id']}")
            move_email_to_trash(record['id'])
            logger.info(f"Deleted email with id {record['id']}")

delete_spam_emails()