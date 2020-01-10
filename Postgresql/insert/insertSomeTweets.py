import psycopg2
import json
import random


SQL = """INSERT INTO tweets VALUES (
    {id},
    {text},
    {user_id},
    {user_name},
    {location},
    {user_friends},
    {user_followers_count}, 
    {timestamp},
    {is_tweet_reply},
    {score},
    {topic}, 
    {telecom_compagny});

"""


def getRequests():
    requetes = []
    with open('./Postgresql/insert/tweets.json') as f:
        data = json.load(f)

        for tweet in data:

            requete = SQL.format(
                id=tweet["id"],
                text=tweet["text"],
                user_id=tweet["user"]["id"],
                user_name=tweet["user"]["screen_name"],
                location=tweet["user"]["location"],
                user_friends=tweet["user"]["friends_count"],
                user_followers_count=tweet["user"]["followers_count"],
                timestamp=tweet["created_at"],
                is_tweet_reply=tweet["in_reply_to_status_id"] != None,
                score=random.uniform(0, 1),
                topic="box" if random.uniform(0, 1) > 0.5 else "mobile",
                telecom_compagny="verizon" if random.uniform(0, 1) > 0.5 else "ATT"
            )
            print(requete)
            requetes.append(requete)
    return requetes


reqs = getRequests()

try:

    connection = psycopg2.connect(user="docker",
                                  password="docker",
                                  host="127.0.0.1",
                                  port="5432",
                                  database="docker")

    cursor = connection.cursor()
    # Print PostgreSQL Connection properties
    print(connection.get_dsn_parameters(), "\n")

    # Print PostgreSQL version
    cursor.execute("SELECT version();")
    record = cursor.fetchone()
    print("You are connected to - ", record, "\n")

except (Exception, psycopg2.Error) as error:
    print("Error while connecting to PostgreSQL", error)
finally:
    #closing database connection.
        if(connection):
            cursor.close()
            connection.close()
            print("PostgreSQL connection is closed")
