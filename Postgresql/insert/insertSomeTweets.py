import sqlalchemy
import psycopg2
import json
import random
from sqlalchemy import Table, Column
import os


def connect(user, password, db, host='localhost', port=5432):
    '''Returns a connection and a metadata object'''
    # We connect with the help of the PostgreSQL URL
    # postgresql://federer:grandestslam@localhost:5432/tennis
    url = 'postgresql://{}:{}@{}:{}/{}'
    url = url.format(user, password, host, port, db)

    # The return value of create_engine() is our connection object
    con = sqlalchemy.create_engine(url, client_encoding='utf8')

    # We then bind the connection to MetaData()
    meta = sqlalchemy.MetaData(bind=con, reflect=True)

    return con, meta


# connect to the database
con, meta = connect('docker', 'docker', 'docker')
# clear existing tables from the meta object
command = "DROP TABLE IF EXISTS data;"
con.execute(command)

meta.clear()

table = Table('data', meta,
              Column('id', sqlalchemy.BigInteger, primary_key=True),
              Column('text', sqlalchemy.VARCHAR(281)),
              Column('user_id', sqlalchemy.BIGINT),
              Column('user_name', sqlalchemy.VARCHAR(100)),
              Column('location', sqlalchemy.VARCHAR(100)),
              Column('user_friends_count', sqlalchemy.INT),
              Column('user_followers_count', sqlalchemy.INT),
              Column('timestamp', sqlalchemy.TIMESTAMP),
              Column('is_tweet_reply', sqlalchemy.BOOLEAN),
              Column('score', sqlalchemy.FLOAT(10)),
              Column('topic', sqlalchemy.VARCHAR(50)),
              Column('telecom_company', sqlalchemy.VARCHAR(50))
              )

meta.create_all(con, checkfirst=True)

with open('tweets.json') as f:
    data = json.load(f)
    print(data[0]["text"])

    for tweet in data:

        clause = table.insert().values(
            id=tweet["id"],
            text=tweet["text"],
            user_id=tweet["user"]["id"],
            user_name=tweet["user"]["screen_name"],
            location=tweet["user"]["location"],
            user_friends_count=tweet["user"]["friends_count"],
            user_followers_count=tweet["user"]["followers_count"],
            timestamp=tweet["created_at"],
            is_tweet_reply=tweet["in_reply_to_status_id"] != None,
            score=random.uniform(0, 1),
            topic="box" if random.uniform(0, 1) > 0.5 else "mobile",
            telecom_company="verizon" if random.uniform(
                0, 1) > 0.5 else "ATT"
        )
        con.execute(clause)
