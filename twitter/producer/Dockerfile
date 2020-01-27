
FROM python:3.6-alpine


COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt
COPY Producer.py Producer.py
ARG kafka_twitter_topic=${kafka_twitter_topic}
ARG docker_kafka_adress=${docker_kafka_adress}
ARG docker_kafka_port=${docker_kafka_port}
ARG docker_postgres_port=${docker_postgres_port}

ARG twitter_consumer_key=${twitter_consumer_key}
ARG twitter_consumer_secret=${twitter_consumer_secret}
ARG twitter_access_token=${twitter_access_token}
ARG twitter_access_token_secret=${twitter_access_token_secret}

# RUN ping 8.8.8.8


RUN echo $kafka_twitter_topic


