chmod 640 neo4j.conf

sudo docker compose up

bin/neo4j-admin import --nodes=data/artists.csv --relationships=data/feats.csv --force