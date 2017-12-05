#!/usr/bin/env bash
# check is production config exists in configs
compose_prod=configs/docker-compose.prod.yml
server_prod=configs/server-config.prod.json
validator_prod=configs/validator-config.prod.json
spider_prod=configs/spider-config.prod.py

if [ ! -f ${compose_prod} ] || [ ! -f ${server_prod} ] || [ ! -f ${validator_prod} ] || [ ! -f ${spider_prod} ] 
then
    echo "installing PyYaml"
    pip install PyYaml
    echo "= = = = = = = = = ="
    echo "Start configuration"
    python3 config.py
    echo "configuration generated, start deploying ... "
fi

echo "First, remove old file ... "
if [ -d deploy ]
then
    sudo rm -rf deploy
fi
if [ -f deploy.tar.gz ]
then
    sudo rm deploy.tar.gz
fi
echo "Secondly, prepare files ... "
mkdir deploy
cp configs/docker-compose.prod.yml deploy/docker-compose.yml


### server
## create server_deploy
mkdir deploy/server
cp -r server/ deploy/server/server
cp -r public/ deploy/server/public
mv deploy/server/server/requirements.txt deploy/server/
mv deploy/server/server/Dockerfile deploy/server/
cp --remove-destination configs/server-config.prod.json deploy/server/server/config.json

## validator
# create server_deploy
mkdir deploy/validator
cp -r validator/ deploy/validator/validator
cp -r public/ deploy/validator/public
mv deploy/validator/validator/requirements.txt deploy/validator/
mv deploy/validator/validator/Dockerfile deploy/validator/
cp --remove-destination configs/validator-config.prod.json deploy/validator/validator/config.json

### spider
## create spider_deploy
mkdir deploy/spider
cp -r spider/ deploy/spider/spider
cp -r public/ deploy/spider/public
mv deploy/spider/spider/requirements.txt deploy/spider/
mv deploy/spider/spider/Dockerfile deploy/spider/
cp --remove-destination configs/spider-config.prod.py deploy/spider/spider/proxy_crawler/settings.py

echo "Create tar.gz file ... "
tar -zcvf deploy.tar.gz deploy

echo "Add credientials ... "
# change here to your key
ssh-add path/to/your/ssh_key
# scp tar file to remote server
scp -P your_server_ssh_port deploy.tar.gz your_username@your_server_address:/some/remote/directory
# start deploying in remote server
ssh your_username@your_server_address -p your_server_ssh_port "cd /some/remote/directory && tar -xzf deploy.tar.gz"
ssh your_username@your_server_address -p your_server_ssh_port "cd /some/remote/directory/deploy && docker-compose up --build"

