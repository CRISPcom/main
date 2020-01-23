import logging, sys, time
from TwitterProducer import *

def main(topic, tracks):
    producer = TwitterProducer(topic, tracks)
    producer.daemon = True
    producer.start()
    while True:
        time.sleep(1)

if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2:])