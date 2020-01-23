# On lance l'architecture de traitement
docker-compose up -d

cd PostGresql/insert/

# On insert les tweets
python insertSomeTweets.py
