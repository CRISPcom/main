from kafka import KafkaConsumer
from json import loads
import os
import time
import logging

logging.basicConfig(filename="error.log", level=logging.INFO)

kafka_twitter_topic=os.environ["kafka_twitter_topic"]
docker_kafka_port=os.environ["docker_kafka_port"]
docker_kafka_adress=os.environ["docker_kafka_adress"]
for i in range(15):
    try:
        consumer = KafkaConsumer(
            kafka_twitter_topic,
            bootstrap_servers=[f'{docker_kafka_adress}:{docker_kafka_port}'],
            auto_offset_reset='earliest',
            enable_auto_commit=True,
            group_id=None,
            value_deserializer=lambda x: loads(x.decode('utf-8')),
        )
        i=15
    except:
        # Wait for kafka to be up
        time.sleep(2)
        logging.warn("Cannot connect to Kafka. Retrying in 2 seconds")


for message in consumer:
    if "text" in message.value:
        logging.info(f"received message : {message.value['text']}")
