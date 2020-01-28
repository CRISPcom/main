
FROM python:3.6-alpine

# Setting up postgres dev environment
RUN apk update && apk add postgresql-dev gcc python3-dev musl-dev
# install dependency
COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

# Copy code
COPY Consumer.py Consumer.py
COPY Insert.py Insert.py

# Set environment variables
ARG kafka_twitter_topic=${kafka_twitter_topic}
ARG docker_kafka_adress=kafka
ARG docker_kafka_port=${docker_kafka_port}
ARG docker_postgres_port=${docker_postgres_port}
