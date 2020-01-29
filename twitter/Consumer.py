from kafka import KafkaConsumer
from json import loads
import os

consumer = KafkaConsumer(
    os.environ['kafka_twitter_topic'],
    bootstrap_servers=['127.0.0.1:9092'],
    auto_offset_reset='earliest',
    enable_auto_commit=True,
    group_id=None,
    value_deserializer=lambda x: loads(x.decode('utf-8')),
)

for message in consumer:
    if "text" in message.value:
        print(message.value["text"])
