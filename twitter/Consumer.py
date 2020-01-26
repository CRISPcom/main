from kafka import KafkaConsumer
from json import loads
consumer = KafkaConsumer(
    'UploadFile',
     bootstrap_servers=['localhost:9092'],
     auto_offset_reset='earliest',
     enable_auto_commit=True,
     group_id=None,
     value_deserializer=lambda x: loads(x.decode('utf-8')),
     )

for message in consumer:
    if "text" in message.value:
        print(message.value["text"])