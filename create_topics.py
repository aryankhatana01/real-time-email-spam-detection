from confluent_kafka.admin import NewTopic
from admin_client import create_admin_client
import config
import time
from _logging import get_logger

logger = get_logger()


def create_kafka_topic(broker_name, topic_names, num_partitions=1, replication_factor=1):
    # Configure the admin client with the bootstrap servers
    admin_client = create_admin_client(broker_name)
    logger.info("Admin client connected to Kafka broker!")

    # Create a list of NewTopic object with topic configuration
    topics_list = []
    for topic in topic_names:
        topics_list.append(NewTopic(topic, num_partitions=num_partitions, replication_factor=replication_factor))

    # Create the topic
    admin_client.create_topics(topics_list)
    time.sleep(10) # Added for safety

if __name__ == "__main__":
    # Kafka broker details
    broker_name = config.KAFKA_BROKER

    # Topic details
    topic_names = [config.EMAILS_TOPIC, config.PREDICTIONS_TOPIC]
    num_partitions = config.NUM_PARTITIONS
    replication_factor = 1
    
    # Create the Kafka topic for transactions
    create_kafka_topic(broker_name, topic_names, num_partitions, replication_factor)

    # print("Kafka topic created successfully")
    logger.info("Kafka topics created successfully!")