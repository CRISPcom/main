#!/usr/bin/python3.6

import logging, time, sys, json, os, codecs
from tweepy import OAuthHandler
from tweepy import Stream
import tweepy as tw
from kafka import KafkaProducer
from kafka import KafkaProducer
from kafka.errors import KafkaError
import nltk
nltk.download('vader_lexicon')
from nltk.sentiment.vader import SentimentIntensityAnalyzer as sia


consumer_key = "key"
consumer_secret = "key"
access_token = "key"
access_token_secret = "key"

TARGET = ["AT&T", "Verizon", "Vodafone", "Comcast"]

class TwitterClient(tw.StreamListener):
  """ A listener handles tweets that are received from the stream."""

  topic = "UploadFile"
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

        # for trac in self.track :
        #     if trac in text :
        #         self.topic = trac
        self.producer.send(
            self.topic, 
            value=json.dumps(status._json),
            key=bytes(status._json["id_str"], 'utf-8')
        ).add_callback(lambda x: sys.stdout.write(str(x) + "\n"))

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
    stream = tw.Stream(auth= api.auth, listener =myStreamListener)
    stream.filter(track= TARGET, languages=["en"])