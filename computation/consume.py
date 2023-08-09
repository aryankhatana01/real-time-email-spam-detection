# This file will become the subsriber of the email topic and write to predictions.
import sys
sys.path.append('../')

import json
from multiprocessing import Process
from utils import create_consumer, create_producer
import config
from _logging import logger
from computation.preprocesser import convert_to_string_and_cleanup, combine_subject_and_body
from inference import inference
from computation.configure_model import get_configured_model
import numpy as np


def predict():
    consumer = create_consumer(topic=config.EMAILS_TOPIC, group_id=config.EMAILS_GROUP_ID)
    producer = create_producer()

    model = get_configured_model()

    while True:
        message = consumer.poll(timeout=400)
        if message is None:
            continue
        if message.error():
            logger.error("Consumer error: {}".format(message.error()))
            continue
        record = json.loads(message.value().decode('utf-8'))
        record = convert_to_string_and_cleanup(record)
        record = combine_subject_and_body(record)
        msg = np.array([record['msg']])
        msgs, predictions, predictions_probs = inference.inference_fn(
            model=model,
            msg=msg
        )
        logger.info(f"Predictions: {predictions}")
        logger.info(f"Message received with ID {record['id']}")

# One consumer per partition
if __name__ == "__main__":
    for _ in range(config.NUM_PARTITIONS):
        p = Process(target=predict)
        p.start()
    # predict()