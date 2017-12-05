## Proxy Management Platform
[![Build Status](https://travis-ci.org/ezirmusitua/PMP.svg?branch=master)](https://travis-ci.org/ezirmusitua/PMP) [![Coverage Status](https://coveralls.io/repos/github/ezirmusitua/proxies/badge.svg?branch=master)](https://coveralls.io/github/ezirmusitua/proxies?branch=master) [![codebeat badge](https://codebeat.co/badges/df7ff88e-719d-4cc9-8257-1bee731bd9c2)](https://codebeat.co/projects/github-com-ezirmusitua-proxies-master)  

A platform to mange your proxies[Still Working]  

### Features
1. Crawl free proxy from internet
2. Validate accessability of proxy
3. An easy to use web app

### Requirements  
python 3+
mongodb 3.2+

### Installation
```bash
# PreInstallation
## mongodb 3.2+
## python 3+
# clone project
git clone git@github.com:ezirmusitua/proxies.git ppm
cd ppm/validator
# download the geolite mmdb for geo detection
curl -O http://geolite.maxmind.com/download/geoip/database/GeoLite2-City.mmdb.gz
```

### Usage  
```bash
# assume in main directory
# run tests  
nosetests server spider validator

proxy_crawler
python crawler/run.py
# run validator
python validator/run.py
# start web app
python server/app.py
```
use in fish shell, add the following code in your ~/.config/fish/config.fish  
```shell
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
  set -l proxy_str (curl "localhost:3080/lucky-proxy?platform=shell&connection=$connection&anonymity=$anonymity")
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

### Development  
<p style="color: red; font-weight: 600">THIS PROJECT IS NOT USABLE AT NOW 2017/11/08</p>  

[](https://docs.mongodb.com/manual/tutorial/enable-authentication/)        
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

[How To Install Docker In Debian 9](https://linuxconfig.org/how-to-install-docker-engine-on-debian-9-stretch-linux)  
[How To Install Docker Compose](https://docs.docker.com/compose/install/#install-compose)  

### Author  
jferroal@gmail.com

### License
MIT for now  

