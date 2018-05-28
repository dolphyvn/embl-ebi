#!/bin/bash

docker pull mongodb
docker volume create mongodb
docker run --name mongodb -p 27017:27017  -v mongodb:/data/db -dti mongo
docker stop restfullapi
docker rm restfullapi
docker build -t restfullapi .
echo "____Start run unit test_____"
docker run -ti --rm --link mongodb:mongodb -p 5000:5000 restfullapi python tests.py
echo "____Starting the application_____"
docker run -dti --name restfullapi --link mongodb:mongodb -p 5000:5000 restfullapi
