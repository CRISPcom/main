
FROM python:3.6-alpine

# install dependency
COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt
# Copy code
COPY Producer.py Producer.py

# Set environment variables
ARG kafka_twitter_topic=${kafka_twitter_topic}
ARG docker_kafka_adress=${docker_kafka_adress}
ARG docker_kafka_port=${docker_kafka_port}
ARG docker_postgres_port=${docker_postgres_port}

ARG twitter_consumer_key=${twitter_consumer_key}
ARG twitter_consumer_secret=${twitter_consumer_secret}
ARG twitter_access_token=${twitter_access_token}
ARG twitter_access_token_secret=${twitter_access_token_secret}
ARG twitter_filter_channel=${twitter_filter_channel}

ARG twitter_feed_channel=${twitter_feed_channel}
