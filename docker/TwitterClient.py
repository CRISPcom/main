from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream
from kafka import KafkaProducer
                from kafka.client import SimpleClient
                from kafka.consumer import SimpleConsumer
                from kafka.producer import SimpleProducer

                client = SimpleClient("localhost:9092")
                producer = SimpleProducer(client)
                consumer_key = "key"
                consumer_secret = "key"
                access_token = "key"
                access_token_secret = "key"

                class StdOutListener(StreamListener):
                """ A listener handles tweets that are received from the stream.
                This is a basic listener that just prints received tweets to stdout.
                """
                  def on_data(self, data):
                    producer.send_messages('movies', str(data))
                    print(data)
                    return True

                  def on_error(self, status):
                    print(status)

                  if __name__ == '__main__':
                    l = StdOutListener()
                    auth = OAuthHandler(consumer_key, consumer_secret)
                    auth.set_access_token(access_token, access_token_secret)
                    stream = Stream(auth, l)
                    stream.filter(track=['#moana'],languages=["en"])