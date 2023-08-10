# This file will become the subsriber of the email topic and write to predictions.
import sys
sys.path.append('../')

import json
from multiprocessing import Process
from utils import create_consumer, create_producer
import config
from _logging import logger
from computation.preprocessor import convert_to_string_and_cleanup, combine_subject_and_body
from inference import inference
from computation.configure_model import get_configured_model
import numpy as np
import datetime
import time

consumer = create_consumer(topic=config.EMAILS_TOPIC, group_id=config.EMAILS_GROUP_ID)
producer = create_producer()
model = get_configured_model()
def predict():

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
        record = convert_to_string_and_cleanup(record)
        record = combine_subject_and_body(record)
        msg = np.array([record['msg']])
        msgs, predictions, predictions_probs = inference.inference_fn(
            model=model,
            msg=msg
        )

        probs_converted_to_list = predictions_probs.numpy().tolist()
        record["probs"] = probs_converted_to_list[0]
        record["prediction"] = predictions.numpy().tolist() # 1 for spam, 0 for ham
        record['timestamp'] = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        pred_record = json.dumps(record).encode('utf-8')

        producer.produce(topic=config.PREDICTIONS_TOPIC,
                         value=pred_record)
        producer.flush()

        logger.info(f"Message received with ID {record['id']}")
        logger.info(f"Predictions: {predictions}")
        logger.info(f"Predictions sent with ID {record['id']}")
        print()
    consumer.close()

# One consumer per partition
# if __name__ == "__main__":
    # for _ in range(config.NUM_PARTITIONS):
    #     p = Process(target=predict)
    #     p.start()
predict()