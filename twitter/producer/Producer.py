#!/usr/bin/python3.6

from kafka.errors import KafkaError
from kafka import KafkaProducer
import tweepy as tw
from tweepy import Stream
from tweepy import OAuthHandler
import codecs
import os
import json
import sys
import time
import logging
from nltk.sentiment.vader import SentimentIntensityAnalyzer as sia
import nltk
<< << << < HEAD: twitter/Producer_tweet.py
<< << << < HEAD
== == == =
== == == =
>>>>>> > b12708a7683c4a7d1d29bf74bc5384d76a2365a0: twitter/producer/Producer.py
>>>>>> > 776075f7adf2b3147389f177c7c61f5901e7cf2f
<< << << < HEAD: twitter/Producer_tweet.py
<< << << < HEAD
# nltk.download('vader_lexicon')


consumer_key = "cW3RTKoG5kiNkzfdbSb8aBMyY"
consumer_secret = "iwj5uOncngUMYk2BMNkF3WwL9VR7FXCPvXJVYwbDNDmuy8yRkH"
access_token = "4175914697-j5Ghb209PGZOkobm0cnh9nZ2zMwrrigfVGczYbA"
access_token_secret = "0lK2XYfh1oksmpymqgTRBLrhR5nGLMUr84N0yhicWuUq2"

TARGET = ["AT&T", "Verizon", "Vodafone", "Comcast"]


class TwitterClient(tw.StreamListener):
    """ A listener handles tweets that are received from the stream."""

    topic = ""
    track = TARGET
    producer = KafkaProducer(
        bootstrap_servers=os.getenv("KAFKA_BROKER", "127.0.0.1:9092"),
        value_serializer=lambda v: json.dumps(v).encode('utf-8'),
        key_serializer=str.encode,
        acks="all",
        retries=2,
    )

    def on_status(self, status):

        try:
            text = status._json["text"]
            ps = sia().polarity_scores(text)
            score = ps["compound"]
            print("tweet : ", score)
            status._json['score'] = score

            """ #Test
        fil = codecs.open("file2.json","w","utf-8")
        fil.write(json.dumps(status._json))
        fil.close()"""

            for trac in self.track:
                if trac in text:
                    self.topic = trac
            self.producer.send(
                self.topic,
                value=json.dumps(status._json),
                key=b'1'
            ).add_callback(lambda x: sys.stdout.write(str(x) + "\n"))

        except StopIteration as e:
            self.producer.close()
            running = False

    def on_error(self, status):
        print(status)


== == == =
== == == =
logging.basicConfig(filename="error.log", level=logging.INFO)
>>>>>> > b12708a7683c4a7d1d29bf74bc5384d76a2365a0: twitter/producer/Producer.py
nltk.download('vader_lexicon')

# Set tweeter auth credentials (from the .env file)
consumer_key = os.environ['twitter_consumer_key']
consumer_secret = os.environ['twitter_consumer_secret']
access_token = os.environ['twitter_access_token']
access_token_secret = os.environ['twitter_access_token_secret']

topic = os.environ['kafka_twitter_topic']
kafka_port = os.environ["docker_kafka_port"]
kafka_adress = os.environ["docker_kafka_adress"]

TARGET = os.environ["twitter_feed_channel"].split(",")
logging.info(f"listening to {TARGET}")


class TwitterClient(tw.StreamListener):
    """ A listener handles tweets that are received from the stream."""

    topic = topic

    def on_status(self, status):
        """
        When the client receives a tweet
            :param status:  the tweet status
        """
        try:
            if "extended_tweet" in status._json and "full_text" in status._json["extended_tweet"]:
                status._json["text"] = status._json["extended_tweet"]["full_text"]
            text = status._json["text"]
            ps = sia().polarity_scores(text)
            score = ps["compound"]
            logging.info(f"tweet : {score}")
            status._json['score'] = score

            for company in TARGET :
                if company in status._json["text"]:
                    status._json["company"]=company

            self.producer.send(
                self.topic,
                value=status._json,
            )

        except StopIteration as e:
            self.producer.close()
            running = False

    def on_error(self, status):


<< << << < HEAD: twitter/Producer_tweet.py
print(status)
>>>>>> > 776075f7adf2b3147389f177c7c61f5901e7cf2f
== == == =
"""
    docstring here
        :param self:
        :param status:
    """
logging.error(status)

>>>>>> > b12708a7683c4a7d1d29bf74bc5384d76a2365a0: twitter/producer/Producer.py


if __name__ == '__main__':
    # We try to connect 15 times before shutting down
    for i in range(15):
        try:
            producer = KafkaProducer(
                bootstrap_servers=f"{kafka_adress}:{kafka_port}",
                value_serializer=lambda v: json.dumps(v).encode('utf-8'),
                acks="all",
                retries=2,
            )
            i = 15
        except:
            time.sleep(2)
            logging.warn("Cannot connect to Kafka. Retrying in 2 seconds")

    auth = OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)
    api = tw.API(auth, wait_on_rate_limit=True)
    myStreamListener = TwitterClient()
<< << << < HEAD: twitter/Producer_tweet.py
<< << << < HEAD
stream = tw.Stream(auth=api.auth, listener=myStreamListener)
stream.filter(track=TARGET, languages=["en"])
== == == =
== == == =
myStreamListener.producer = producer
>>>>>> > b12708a7683c4a7d1d29bf74bc5384d76a2365a0: twitter/producer/Producer.py
stream = tw.Stream(auth=api.auth, listener=myStreamListener)
stream.filter(track=TARGET, languages=["en"])
>>>>>> > 776075f7adf2b3147389f177c7c61f5901e7cf2f
