from confluent_kafka.admin import AdminClient
import config
from admin_client import create_admin_client
import argparse
from _logging import get_logger

logger = get_logger()


def delete_kafka_topics(broker_name, topics):
    admin_client = create_admin_client(broker_name)
    logger.info("Admin client connected to Kafka broker!")

    fs = admin_client.delete_topics(topics, operation_timeout=30)

    # Wait for operation to finish.
    for topic, f in fs.items():
        try:
            f.result()  # The result itself is None
            logger.info("Topic {} deleted".format(topic))
        except Exception as e:
            logger.info("Failed to delete topic {}: {}".format(topic, e))

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Delete Kafka topics")
    parser.add_argument("topics", nargs="+", help="List of topic names to delete")
    args = parser.parse_args()

    # Kafka broker details
    broker_name = config.KAFKA_BROKER

    # Topic details
    # topic_names = ["anomalies", "transactions"]
    topic_names = args.topics

    # Delete the Kafka topics
    delete_kafka_topics(broker_name, topic_names)