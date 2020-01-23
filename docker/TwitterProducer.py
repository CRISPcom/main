import threading, logging, time, sys, json
from kafka import KafkaProducer
from kafka.errors import KafkaError
from TwitterClient import *

class TwitterProducer(threading.Thread):
    topic = ""
    track = ["sfr", "orange"]
    producer = None
    t = None
    
    def __init__(self, topic, track):
        self.topic = topic
        self.track = track
        threading.Thread.__init__(self)
        self.stop_event = threading.Event()
        self.t = TwitterClient()

        self.producer = KafkaProducer(
            bootstrap_servers=os.getenv("KAFKA_BROKER", "127.0.0.1:9092"),
            value_serializer=lambda v: json.dumps(v).encode('utf-8'),
            key_serializer=str.encode,
            acks="all",
            retries=sys.maxint,
            
        )

    def stop(self):
        self.producer.close()
        self.stop_event.set()
        

    def run(self):
        stream = self.t.stream(self.track)
        running = True
        while running:
            try:
                text = next(stream)
                self.producer.send(
                    self.topic, 
                    value=text.encode(encoding="UTF-8"),
                    key=b'1'
                ).add_callback(lambda x: sys.stdout.write(str(x) + "\n"))
            except StopIteration as e:
                self.producer.close()
                running = False