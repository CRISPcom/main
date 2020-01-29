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
* nltk NLP models with VADER lexicon

## Getting started
### Limitations
This project only works only works on Linux OS for now.

### Launch
1. Clone the repository : git clone https://github.com/CRISPcom/main.git
2. Go to cloned folder `cd main`
3. Install dependencies : `pip install -r requirements.txt`
4. Launch projet  : `source start.sh`