## Proxy Management Platform
[![Build Status](https://travis-ci.org/ezirmusitua/proxies.svg?branch=master)](https://travis-ci.org/ezirmusitua/proxies) [![Coverage Status](https://coveralls.io/repos/github/ezirmusitua/proxies/badge.svg?branch=master)](https://coveralls.io/github/ezirmusitua/proxies?branch=master) [![codebeat badge](https://codebeat.co/badges/df7ff88e-719d-4cc9-8257-1bee731bd9c2)](https://codebeat.co/projects/github-com-ezirmusitua-proxies-master)
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
# assume in ppm main directory
# run crawler
python crawler/run.py
# run validator
python validator/run.py
# start web app
python server/app.py
```

### Development
<p style="color: red; font-weight: 600">THIS PROJECT IS NOT USABLE AT NOW 2017/11/08</p>

### Author
jferroal@gmail.com

### License
MIT for now

