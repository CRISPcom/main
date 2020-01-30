import geocoder
import logging
import json
logging.basicConfig(filename="error.log", level=logging.INFO)


def geocode(tweet):
    """
    Geocodes a tweet based on his user location.
    Checks if user has defined his location

        :param tweet: the tweet to encode
        :returns: dic with keys `country`, `lat`, `lon`
    """
    result = {
        "country":"",
        "lat":0,
        "lon":0
    }
    if "user" in tweet and tweet["user"]["location"] is not None:
        userLocation = tweet["user"]["location"]
        try:
            g = geocoder.osm(userLocation)
            # We only add some data if accuracy is over a certain level (Arbitrary)
            if g.json["accuracy"] > 0.3:
                result["country"] = g.json['raw']["address"]["country_code"]
                result["lat"] = g.json['raw']["lat"]
                result["lon"] = g.json['raw']["lon"]
                print(userLocation, result)
        except:
            logging.error(f"An error happenened when trying to get user location : {userLocation}")
    return result

