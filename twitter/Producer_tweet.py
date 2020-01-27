#!/usr/bin/python3.6

from nltk.sentiment.vader import SentimentIntensityAnalyzer as sia
import logging
import time
import sys
import json
import os
import codecs
from tweepy import OAuthHandler
from tweepy import Stream
import tweepy as tw
from kafka import KafkaProducer
from kafka import KafkaProducer
from kafka.errors import KafkaError
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


if __name__ == '__main__':
    auth = OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)
    api = tw.API(auth, wait_on_rate_limit=True)
    myStreamListener = TwitterClient()
    stream = tw.Stream(auth=api.auth, listener=myStreamListener)
    stream.filter(track=TARGET, languages=["en"])
