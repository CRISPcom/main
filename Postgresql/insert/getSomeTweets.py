import tweepy
import json
import codecs


# auth settings
Consumer_key = 'KEY'
Consumer_secret = 'KEY'
Access_token = 'KEY'
Access_token_secret = 'KEY'


ORIGINAL_POOL = ['verizon', 'ATT', 'Vodafone', 'Comcast']


auth = tweepy.OAuthHandler(Consumer_key, Consumer_secret)
auth.set_access_token(Access_token, Access_token_secret)
api = tweepy.API(auth)


class StreamListener(tweepy.StreamListener):
    nbTweets = 0
    tweets = []
    def on_status(self, status):

        print(status.text)
        self.tweets.append(status._json)
        self.nbTweets+=1
        if self.nbTweets == 50:
            file_ = codecs.open(f"tweets.json","w","utf-8")
            file_.write(json.dumps(self.tweets))
            file_.close()
            exit()

    def on_error(self, status_code):
        if status_code == 420:
            exit()
            return False


auth = tweepy.OAuthHandler(Consumer_key, Consumer_secret)
auth.set_access_token(Access_token, Access_token_secret)
api = tweepy.API(auth)


stream_listener = StreamListener()
stream = tweepy.Stream(auth=api.auth, listener=stream_listener,)
stream.filter(track=ORIGINAL_POOL, languages=["en"])
