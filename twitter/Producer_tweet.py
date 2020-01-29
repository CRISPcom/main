#!/usr/bin/python3.6

<<<<<<< HEAD
import logging, time, sys, json, os, codecs
=======
from nltk.sentiment.vader import SentimentIntensityAnalyzer as sia
import logging
import time
import sys
import json
import os
import codecs
>>>>>>> 776075f7adf2b3147389f177c7c61f5901e7cf2f
from tweepy import OAuthHandler
from tweepy import Stream
import tweepy as tw
from kafka import KafkaProducer
from kafka import KafkaProducer
from kafka.errors import KafkaError
<<<<<<< HEAD
# nltk.download('vader_lexicon')
from nltk.sentiment.vader import SentimentIntensityAnalyzer as sia


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
        text=status._json["text"]
        ps = sia().polarity_scores(text)
        score=ps["compound"]
        print("tweet : ",score)
        status._json['score'] = score

        """ #Test
        fil = codecs.open("file2.json","w","utf-8")
        fil.write(json.dumps(status._json))
        fil.close()"""

        for trac in self.track :
            if trac in text :
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
=======
import nltk
nltk.download('vader_lexicon')


consumer_key = os.environ['twitter_consumer_key']
print(consumer_key)
consumer_secret = os.environ['twitter_consumer_secret']
access_token = os.environ['twitter_access_token']
access_token_secret = os.environ['twitter_access_token_secret']

TARGET = ["AT&T", "Verizon", "Vodafone", "Comcast"]


class TwitterClient(tw.StreamListener):
    """ A listener handles tweets that are received from the stream."""

    topic = os.environ['kafka_twitter_topic']
    track = TARGET
    producer = KafkaProducer(
        bootstrap_servers=os.getenv("KAFKA_BROKER", "127.0.0.1:9092"),
        value_serializer=lambda v: json.dumps(v).encode('utf-8'),
        acks="all",
        retries=2,
    )

    def on_status(self, status):

        try:
            if "extended_tweet" in status._json and "full_text" in status._json["extended_tweet"]:
                status._json["text"] = status._json["extended_tweet"]["full_text"]
            text = status._json["text"]
            ps = sia().polarity_scores(text)
            score = ps["compound"]
            print("tweet : ", score)
            status._json['score'] = score

            self.producer.send(
                self.topic,
                value=status._json,
            )

        except StopIteration as e:
            self.producer.close()
            running = False

    def on_error(self, status):
        print(status)
>>>>>>> 776075f7adf2b3147389f177c7c61f5901e7cf2f


if __name__ == '__main__':
    auth = OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)
    api = tw.API(auth, wait_on_rate_limit=True)
    myStreamListener = TwitterClient()
<<<<<<< HEAD
    stream = tw.Stream(auth= api.auth, listener =myStreamListener)
    stream.filter(track= TARGET, languages=["en"])
=======
    stream = tw.Stream(auth=api.auth, listener=myStreamListener)
    stream.filter(track=TARGET, languages=["en"])
>>>>>>> 776075f7adf2b3147389f177c7c61f5901e7cf2f
