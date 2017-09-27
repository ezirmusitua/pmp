# -*- coding: utf-8 -*-
import geoip2.database


class IpGeo(object):
    __db_reader = geoip2.database.Reader('./GeoLite2-City.mmdb')

    def __init__(self, ip_address, locale='en'):
        self._ip_address = ip_address
        self._locale = locale
        self.info = IpGeo.read(ip_address)

    @property
    def ip_address(self):
        return self.ip_address

    @property
    def locale(self):
        return self._locale

    @property
    def country(self):
        return self.info['country']

    @property
    def city(self):
        return self.info['city']

    @property
    def location(self):
        return self.info['location']

    @property
    def postal(self):
        return self.info['postal']

    @property
    def location_label(self, tmpl='{country}, {city}'):
        return tmpl.format(country=self.info['country'].names[self.locale], city=self.info['city'].names[self.locale])

    @property
    def timezone(self):
        return self.info['location'].timezone

    @property
    def position(self, tmpl='({latitude}, {longitude})'):
        return tmpl.format(latitude=self.info['location'].latitude, longitude=self.info['location'].longitude)

    @property
    def postal_code(self, most=True):
        postal_code = self.info['postal'].code
        if most is True:
            return postal_code
        code_confidence = self.info['postal'].confidence
        if code_confidence < 33:
            desc = 'may be {code}'.format(code=postal_code)
        elif code_confidence < 66:
            desc = 'probably {code}'.format(code=postal_code)
        else:
            desc = 'must be {code}'.format(code=postal_code)
        return {
            'desc': desc,
            'code': postal_code
        }

    @classmethod
    def read(cls, ip_address):
        response = cls.__db_reader.city(ip_address)
        return {
            'country': response.country,
            'city': response.city,
            'location': response.location,
            'postal': response.postal,
        }
