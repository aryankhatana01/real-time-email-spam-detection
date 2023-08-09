# This file will become the subsriber of the email topic and write to predictions.
import sys
sys.path.append('../')

import json
from multiprocessing import Process
from utils import create_consumer, create_producer
import config
from _logging import logger
from preprocesser import convert_to_string_and_cleanup

consumer = create_consumer(topic=config.EMAILS_TOPIC, group_id=config.EMAILS_GROUP_ID)
producer = create_producer()

while True:
    message = consumer.poll(timeout=50)
    if message is None:
        continue
    if message.error():
        logger.error("Consumer error: {}".format(message.error()))
        continue
    record = json.loads(message.value().decode('utf-8'))
    record = convert_to_string_and_cleanup(record)
    logger.info(f"Message received with ID {record['id']}")