# On lance l'architecture de traitement
docker-compose up -d

cd PostGresql/insert/

# On insert les tweets
python insertSomeTweets.py

# configure docker for remote connexions 
sudo systemctl edit docker.service

# put in nano
[Service]
ExecStart=
ExecStart=/usr/bin/dockerd -H fd:// -H tcp://127.0.0.1:2375

# save the file (ctrl+x)

sudo systemctl daemon-reload
sudo systemctl restart docker.service
# check for 0.0.0.0
sudo netstat -lntp | grep dockerd
