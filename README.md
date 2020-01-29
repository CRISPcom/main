# CrispCom : main project

## About
CrisCom analyses tweets for different telecom provider (ATT, Verizon...)
It provides 2 dashboards :
* Real time dashboards, with one dashboard per provider
* Consolidated Dashboard with data over time

# Built with
* Python 3.6
* Docker and docker-compose
* PostgreSQL, Kafka
* Tableau, Grafana
* [nltk](https://www.nltk.org/)  with [VADER](http://www.nltk.org/_modules/nltk/sentiment/vader.html) lexicon

## Getting started

### Requirements
* [docker](https://www.docker.com/)
* [docker compose](https://docs.docker.com/compose/)
* This project has only been tested on linux/unix OS.

### Launch
1. Clone the repository : git clone https://github.com/CRISPcom/main.git
2. Go to cloned folder `cd main`
3. Configure keys in the `.env` file (Most importantly twitter API keys)
3. Launch projet  : `docker-compose up`
4. Enjoy rour real time dashboard (TODO)

## TODO
- [] Add documentation
- [] Add dashboarding (real time and consolidated)
- [] Filter tweets