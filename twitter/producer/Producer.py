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
import logging
logging.basicConfig(filename="error.log", level=logging.INFO)

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
company_username = os.environ["twitter_filter_channel"].split(",")

class TwitterClient(tw.StreamListener):
    """ A listener handles tweets that are received from the stream."""

    topic = topic
    company_username = company_username
    dict_username = {"ATT":"AT&T","ATTHelp":"AT&T","ATTTHANKS":"AT&T","Verizon":"Verizon","VZWSupport":"Verizon","TMobile":"T-Mobile","TMobileHelp":"T-Mobile","VodafoneIT":"Vodafone"}
    producer=None

    def on_status(self, status):
        """
        When the client receives a tweet
            :param status:  the tweet status
        """
        try:
            if status._json["user"]["name"] not in company_username :
                if "extended_tweet" in status._json and "full_text" in status._json["extended_tweet"]:
                    status._json["text"] = status._json["extended_tweet"]["full_text"]
                text = status._json["text"]
                ps = sia().polarity_scores(text)
                score = ps["compound"]
                logging.info(f"tweet : {score}")
                status._json['score'] = score

                # Finding the company the tweet is about
                status._json["company"] = "Unknown"
                if status._json["entities"]["user_mentions"] in company_username :
                    status._json["company"] = dict_username[status._json["entities"]["user_mentions"]]
                else : 
                    for company in TARGET :
                        if company in text :
                            status._json["company"] = company

                self.producer.send(
                    self.topic,
                    value=status._json,
                )

        except StopIteration as e:
            self.producer.close()
            running = False

    def on_error(self, status):
        """
            docstring here
                :param self:
                :param status:
            """
        logging.error(status)

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
    myStreamListener.producer=producer
    stream = tw.Stream(auth=api.auth, listener=myStreamListener)
    stream.filter(track=TARGET, languages=["en"])

