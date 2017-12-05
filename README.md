## Proxy Management Platform
[![Build Status](https://travis-ci.org/ezirmusitua/PMP.svg?branch=master)](https://travis-ci.org/ezirmusitua/PMP) [![Coverage Status](https://coveralls.io/repos/github/ezirmusitua/proxies/badge.svg?branch=master)](https://coveralls.io/github/ezirmusitua/proxies?branch=master) [![codebeat badge](https://codebeat.co/badges/df7ff88e-719d-4cc9-8257-1bee731bd9c2)](https://codebeat.co/projects/github-com-ezirmusitua-proxies-master)  

Collect, Validate, Use Proxy

### Features
1. Crawl free proxy from internet
2. Validate proxy
3. Use proxy

### Requirements
The minimal requirement is:   
1. [python 3+](https://www.python.org/)  
2. [mongodb 3.2+](https://www.mongodb.com/)  

May be you can use docker 17+ too  
[Docker](https://www.docker.com/)  

### Installation  
First, install [Python3+](https://www.python.org/downloads/)  
Second, install [Mongodb3.2+](https://www.mongodb.com/download-center)  
Maybe, install [Docker](https://www.docker.com/)  
Then, clone code from github and download the necessary [resource](http://geolite.maxmind.com/download/geoip/database/) 
```bash
git clone git@github.com:ezirmusitua/pmp.git
cd pmp/validator
# download the geolite mmdb for geo detection
curl -O http://geolite.maxmind.com/download/geoip/database/GeoLite2-City.mmdb.gz
```

### Usage  
#### Use in local host
```bash
# go to the pmp project directory
cd path/to/pmp
# install the dependencies
python3 -m pip install -r requirements.dev.txt   
# run spider
cd pmp/spider  
python3 scheduler.py
# run validator
cd pmp/validator
python validator/scheduler.py
# run server
python server/run.py
```  
#### Deploy to remote server  
First, you should install the necessary tools in your remote server:
1. [Docker](https://linuxconfig.org/how-to-install-docker-engine-on-debian-9-stretch-linux)
2. [docker-compose](https://docs.docker.com/compose/install/#install-compose)  

And, may be you should install ufw in your remote server to update firewall setting  
```bash
apt install ufw  
ufw enable  
ufw allow ...# allow the necessary port 
```
Then, run the deploy.sh in the project root  
```bash  
# before run deploy, remember to update the necessary info in deploy.sh  
bash deploy.sh  
# answer the question to generate configurations  
# wait  
```
After deploy is done, you can run the following to test is work properly  
```bash
mongo mongo_admin:mongo_pass@remote_address:your_mongo_port  
curl "remote_address:server_port/lucky-proxy?platform=shell"  
```
#### Some Tips  
If you use fish shell, add the following code in your ~/.config/fish/config.fish to set proxy easily  
```bash
# proxy setter
function setproxy --argument-names 'connection' 'anonymity'
  # connection query for
  if test -n "$connection"
    set -l connection ""
  end
  # anonymity query for
  if test -n "$anonymity"
    set -l anonymity ""
  end
  # query PMP for a query
  # change localhost:3080 to your server address
  set -l proxy_str (curl "localhost:3080/lucky-proxy?platform=shell&connection=$connection&anonymity=$anonymity&token-key=123123")
  # set shell http_proxy/https_proxy env var
  set -g -x http_proxy "http://$proxy_str"
  set -g -x https_proxy "https://$proxy_str"
end
function unsetproxy
  set -g -e http_proxy
  set -g -e https_proxy
end
# the following line make sure every time the shell start up with not proxy set
unsetproxy
```  

**Remember you should replace some code(like localhost:3080 to your remote_address:server_port)**  

**And for use this, use curl -XPOST "remote_address:server_port/token?username=<server_admin>&password=<server_admin_pwd>" to registry a key to server, and replace in above example"**
  
Try it:  
```bash
fish
setproxy  
```  

If you want to use it in spider or anything else, just try:  
```bash
curl "localhost:3080/lucky-proxy?connection=$connection&anonymity=$anonymity&token-key=123123&size=100"
```  
it will return some proxies to you  

**Recommended: Enable mongo auth if you use in local host**  
```shell  
# create admin user  
use admin  
db.createUser(  
  {  
    user: "dbAdmin",  
    pwd: "123123",  
    roles: [ { role: "userAdminAnyDatabase", db: "admin" } ]  
  }  
)  
# create user for database  
use pmp  
db.createUser(  
  {  
    user: "pmpDbAdmin",  
    pwd: "123123",  
    roles: [ { role: "readWrite", db: "pmp" } ]  
  }  
)  
# edit mongo config  
sudo vim /etc/mongd.conf  
# in config file, add following line    
security:  
  authorization: enabled  
# restart mongo service  
sudo service mongod restart  
```  

### Development          
For development, do the installation at first  
```bash
# run tests  
nosetests validator spider server public  
```  
`pmp/public` include the public part in other module, such as Database, ProxyModel, Utils, Config  
`pmp/server` include the server code, encapsulate bottle.py in app.py, update models.py/route.py to add more functions, you can set mongo info and other related settings in config.json  
`pmp/spider` include the scrapy spider and scheduler, the interval and mongo info are in the scrapy-settings.py    
`pmp/validator` include the validator code, now is simple and maybe useless, replace it or extend by adding function to validation, you can set mongo info and other related settings in config.json  
`pmp/config.py` this file use to collect and generate user config for deploying, you can change or extend it  
`pmp/configs` include the config template for deploying   

### Author  
jferroal@gmail.com

### License
MIT

