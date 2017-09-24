# -*- coding: utf8 -*-
import re
import time

import geoip2.database as geo_db
from client import Client
from database import Database

Connection_Validation_Targets = {
    'GOOGLE': 'https://www.google.com',
    'HTTPBIN': 'https://httpbin.org',
}
Detect_Tool_Site = 'http://www.xxorg.com/tools/checkproxy/'
R_A_PATTERN = re.compile(r'REMOTE_ADDR:(.*?)<br>')
H_V_PATTERN = re.compile(r'HTTP_VIA:(.*?)<br>')
H_X_F_F_PATTERN = re.compile('HTTP_X_FORWARDED_FOR:(.*?)<br>')
__db_reader = geo_db.Reader('../GeoLite2-City.mmdb')
Detect_Target = 'https://httpbin.org/get'
# Proxy_Types = ['http', 'https', 'socks4', 'socks5']
Proxy_Types = ['http']
LOCAL_IP_ADDR = '140.206.71.62'


class ProxyModel(object):
    _database = Database()
    _client = Client()
    _db_reader = geo_db.Reader('../GeoLite2-City.mmdb')
    _doc_cache_size = 1
    _doc_to_remove_cache = {}
    _doc_to_update_cache = {}

    def __init__(self, doc_from_db=None):
        doc = doc_from_db if doc_from_db is not None else {}
        self.id = doc.get('_id', '')
        self.anonymity = doc.get('anonymity', 'unknown').lower()
        self.ip_address = doc.get('ip_address', 'unknown').lower()
        self.port = doc.get('port', -1)
        self.last_check_at = time.time() * 1000  # convert to ms
        self.location = doc.get('location', 'unknown, unknown').lower()
        self.type = doc.get('type', 'unknown').lower()
        self.available_sites = list()
        self.need_to_handle = True

    def proxy_str(self):
        return self.ip_address + ':' + str(self.port)

    def validate_type(self):
        type_validation = ProxyModel.detect_proxy_type(self)
        if type_validation['action'] == 'remove':
            self.need_to_handle = False
            ProxyModel._doc_to_remove_cache[self.proxy_str()] = self.id
        else:
            self.type = type_validation['type']

    def validate_connection(self):
        connection_validation = ProxyModel.detect_connection(self)
        self.available_sites = connection_validation['sites']

    def validate(self):
        """validate all requirements of proxy and save to db"""
        self.validate_type()
        if self.need_to_handle is True:
            self.validate_connection()
            self.anonymity = ProxyModel.detect_anonymity(self)
            self.location = ProxyModel.detect_location(self)
            ProxyModel._database.find_one_and_update({'_id': self.id}, {'$set': self.to_json()})
        if len(ProxyModel._doc_to_remove_cache) >= ProxyModel._doc_cache_size:
            print('docs to remove: ', self._doc_to_remove_cache.values())
            ProxyModel.flush_docs()

    def to_json(self):
        return {
            'anonymity': self.anonymity,
            'ip_address': self.ip_address,
            'port': self.port,
            'last_check_at': self.last_check_at,
            'location': self.location,
            'available_sites': self.available_sites,
            'type': self.type
        }

    def __unicode__(self):
        return self.proxy_str()

    def __str__(self):
        return self.proxy_str()

    def __repr__(self):
        return self.proxy_str()

    @staticmethod
    def detect_connection(proxy):
        """validate connection of proxy"""
        available_sites = list()
        ProxyModel._client.set_proxies(proxy.proxy_str(), proxy.type)
        for site in Connection_Validation_Targets:
            try:
                ProxyModel._client.get(Connection_Validation_Targets[site])
                available_sites.append(site)
            except Exception as e:
                print(e)
        return {'sites': available_sites}

    @staticmethod
    def detect_anonymity(proxy):
        """evaluate the anonymity of proxy"""
        ProxyModel._client.set_proxies(proxy.proxy_str(), proxy.type)
        try:
            content = ProxyModel._client.get(Detect_Tool_Site)
            remote_address = re.search(R_A_PATTERN, content).groups()[0].strip()
            ra_is_proxy = remote_address == proxy.ip_address
            via = re.search(H_V_PATTERN, content).groups()[0].strip()
            via_is_empty = via == ''
            via_is_proxy = via == proxy.ip_address
            x_forwarded_for = re.search(H_X_F_F_PATTERN, content).groups()[0].strip()
            xff_is_empty = x_forwarded_for == ''
            xff_is_proxy = x_forwarded_for == proxy.ip_address
            xff_is_lc = x_forwarded_for == LOCAL_IP_ADDR
            xff_is_rand = not xff_is_lc and not xff_is_proxy and not xff_is_empty
            if ra_is_proxy and via_is_empty and xff_is_empty:
                return 'elite'
            if ra_is_proxy and via_is_proxy and xff_is_rand:
                return 'distorting'
            if ra_is_proxy and via_is_proxy and xff_is_proxy:
                return 'anonymous'
            if ra_is_proxy and via_is_proxy and xff_is_lc:
                return 'transparent'
            return 'unknown'
        except Exception as e:
            print(e)
            return 'unknown'

    @staticmethod
    def detect_location(proxy):
        """adjust location using geo lite"""
        location = ''
        geo = ProxyModel._db_reader.city(proxy.ip_address)
        country = geo.country.names['en']
        if country is not None:
            location += country + ', '
        else:
            location += 'unknown, '
        city = geo.city.name
        if city is not None:
            location += city
        else:
            location += 'unknown'
        return location

    @staticmethod
    def detect_proxy_type(proxy):
        """detect proxy type"""
        proxy_type = 'unknown'
        for ptype in Proxy_Types:
            ProxyModel._client.set_proxies(proxy.proxy_str(), ptype)
            try:
                ProxyModel._client.get(Detect_Target)
                proxy_type = ptype
            except Exception as e:
                print(e)
        return {'action': 'remove' if proxy_type == 'unknown' else 'update', 'type': proxy_type}

    @classmethod
    def flush_docs(cls):
        print(list(cls._doc_to_remove_cache.values()))
        cls._database.remove({'_id': {'$in': list(cls._doc_to_remove_cache.values())}})
        cls._doc_to_remove_cache = {}
