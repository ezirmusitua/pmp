# -*- coding:utf-8 -*-
import os


def ip_geo_info_display_exporter(ip_geo):
    return {
        'ip address: ', ip_geo.ip_address,
        'location: ', ip_geo.location(),
        'zip code: ', ip_geo.zip_code
    }


class Tool(object):
    def __init__(self, name, display=None):
        self.name = name
        self.display = {} if display is None else display

    @property
    def json(self):
        return {
            'name': self.name,
            'display': self.display
        }


from getIpGeoInfo import IpGeo

IpGeo.open_reader(os.path.split(os.path.realpath(__file__))[0] + '/GeoLite2-City.mmdb')
