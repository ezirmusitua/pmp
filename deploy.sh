#!/usr/bin/env bash
sudo rm -rf pmp
mkdir pmp
cp docker-compose.yml pmp/
# server
# create server_deploy
mkdir pmp/server_deploy
# copy server source to server_deploy
cp -r server/ pmp/server_deploy/server
# copy public to server_deploy
cp -r public/ pmp/server_deploy/public
mv pmp/server_deploy/server/requirements.txt pmp/server_deploy/
mv pmp/server_deploy/server/Dockerfile pmp/server_deploy/

# validator
# create server_deploy
mkdir pmp/validator_deploy
# copy server source to server_deploy
cp -r validator/ pmp/validator_deploy/validator
# copy public to server_deploy
cp -r public/ pmp/validator_deploy/public
mv pmp/validator_deploy/validator/requirements.txt pmp/validator_deploy/
mv pmp/validator_deploy/validator/Dockerfile pmp/validator_deploy/
