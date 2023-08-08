from confluent_kafka.admin import AdminClient
from _logging import get_logger

logger = get_logger()

def wait_for_admin_client(admin_client):
    # Wait until the admin client is connected to the Kafka cluster
    while True:
        metadata = admin_client.list_topics(timeout=5)
        if metadata is not None:
            break
        admin_client.poll(0.1)

def create_admin_client(broker_name):
    admin_client = AdminClient({
        'bootstrap.servers': broker_name
    })
    wait_for_admin_client(admin_client)
    logger.info("Admin client connected to Kafka broker!")
    return admin_client