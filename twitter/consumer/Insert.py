import sqlalchemy
import psycopg2
import json
import random
from sqlalchemy import Table, Column
import os
import logging
import Geocode

logging.basicConfig(filename="error.log", level=logging.INFO)


USER = os.getenv("docker_postgres_user", "docker")
PASSWORD = os.getenv("docker_postgres_password", "docker")
DATABASE = os.getenv("docker_postgres_db", "docker")
TABLE = os.getenv("docker_postgres_table", "table")
HOSTNAME = os.getenv("docker_postgres_hostname", "localhost")
PORT = os.getenv("docker_postgres_port", 5432)


def getTable(meta):
    """
    Creates the SQLAlchemy table object
        :param meta: the database metadata
    """
    return Table(TABLE, meta,
          Column('id', sqlalchemy.Integer, primary_key=True),
          Column('text', sqlalchemy.VARCHAR(500)),
          Column('user_id', sqlalchemy.BIGINT),
          Column('user_name', sqlalchemy.VARCHAR(100)),
          Column('location', sqlalchemy.VARCHAR(100)),
          Column('user_friends_count', sqlalchemy.INT),
          Column('user_followers_count', sqlalchemy.INT),
          Column('timestamp', sqlalchemy.TIMESTAMP),
          Column('is_tweet_reply', sqlalchemy.BOOLEAN),
          Column('score', sqlalchemy.FLOAT(10)),
          Column('topic', sqlalchemy.VARCHAR(50)),
          Column('telecom_company', sqlalchemy.VARCHAR(50)),
          Column('lat', sqlalchemy.FLOAT(12)),
          Column('lon', sqlalchemy.FLOAT(12)),
          Column('hashtag', sqlalchemy.VARCHAR(50)),
          extend_existing=True
          )


def connect(user, password, db, host=HOSTNAME, port=PORT):
    """
    Returns a connection and a metadata object
        :param user: the database username
        :param password: the database password
        :param db: the database we'd like to connect to
        :param host: the database adress/hostname
        :param port: the datase port
    """
    # We connect with the help of the PostgreSQL URL
    # postgresql://federer:grandestslam@localhost:5432/tennis
    url = 'postgresql://{}:{}@{}:{}/{}'
    url = url.format(user, password, host, port, db)

    # The return value of create_engine() is our connection object
    con = sqlalchemy.create_engine(url, client_encoding='utf8')

    # We then bind the connection to MetaData()
    meta = sqlalchemy.MetaData(bind=con, reflect=True)

    return con, meta


def init_table():
    """
    Init the table we'll use to insert tweets
    return the connection to the database
    """
    # connect to the database
    con, meta = connect(USER, PASSWORD, DATABASE)
    logging.info("Connected to dabase")
    table = getTable(meta)


    meta.create_all(con, checkfirst=True)
    logging.info("created table")
    return con, table
    
def insertTweet(con, table, tweet):
    """
    Insert one tweet to the dabatase table
        :param con: the database connection
        :param table: the table 
        :param tweet: the tweet
    """
    locationDict = Geocode.geocode(tweet)
    clause = table.insert().values(
            # id=tweet["id"],
            text=tweet["text"],
            user_id=tweet["user"]["id"],
            user_name=tweet["user"]["screen_name"],
            location=locationDict["country"],
            user_friends_count=tweet["user"]["friends_count"],
            user_followers_count=tweet["user"]["followers_count"],
            timestamp=tweet["created_at"],
            is_tweet_reply=tweet["in_reply_to_status_id"] != None,
            score=tweet["score"],
            topic="box" if random.uniform(0, 1) > 0.5 else "mobile",
            telecom_company="verizon" if random.uniform(
                0, 1) > 0.5 else "ATT",
            lat=locationDict["lat"],
            lon=locationDict["lon"],
            hashtag=tweet["entities"]["hashtags"]["text"],
        )
    con.execute(clause)
