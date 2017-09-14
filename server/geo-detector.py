# -*- coding: utf-8 -*-
import geoip2.database as geo_db


class IpGeo(object):
    __db_reader = geo_db.Reader('../GeoLite2-City.mmdb')

    def __init__(self, ip, lang='zh-CN'):
        geo = IpGeo.__db_reader.city(ip)
        self.country = geo.country.names[lang]
        self.city = geo.city.names[lang]

    def join(self):
        return self.country + ', ' + self.city
