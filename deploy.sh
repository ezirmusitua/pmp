#!/usr/bin/env bash
mkdir pmp_deploy
cp docker-compose.yml pmp_deploy
# deploy server
# create server_deploy
mkdir pmp_deploy/server_deploy
# copy server source to server_deploy
cp -r server/ pmp_deploy/server_deploy/server
# copy public to server_deploy
cp -r public/ pmp_deploy/server_deploy/public
mv pmp_deploy/server_deploy/server/requirements.txt pmp_deploy/server_deploy/
mv pmp_deploy/server_deploy/server/Dockerfile pmp_deploy/server_deploy/
# run docker buid
#sudo docker build .
# run docker run
