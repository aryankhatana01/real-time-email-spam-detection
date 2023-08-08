from confluent_kafka.admin import AdminClient
import config
from admin_client import create_admin_client
from _logging import get_logger

logger = get_logger()

def list_kafka_topics(broker_name):
    # Configure the admin client with the bootstrap servers
    admin_client = create_admin_client(broker_name)
    logger.info("Admin client connected to Kafka broker!")

    # List the topics
    topics = admin_client.list_topics(timeout=5)
    return topics.topics

if __name__ == "__main__":
    # Kafka broker details
    broker_name = config.KAFKA_BROKER

    # List the Kafka topics
    topics = list_kafka_topics(broker_name)
    print(topics)