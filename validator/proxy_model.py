# -*- coding: utf8 -*-
import re
import time
import logging

import geoip2.database as geo_db
from client import Client
from database import Database
from requests.exceptions import RequestException

Connection_Validation_Targets = {
    'GOOGLE': 'https://www.google.com',
    'FACEBOOK': 'https://www.facebook.com',
    'YOUTUBE': 'https://www.youtube.com',
    'HTTPBIN': 'https://httpbin.org',
    'BAIDU': 'https://baidu.com',
    'LIAOYUAN': 'https://liaoyuan.io',
    'TAOBAO': 'https://www.taobao.com',
    'CNPROXY': 'http://cn-proxy.com',
    'PREMPROXY': 'https://premproxy.com',
    'PROXYDB': 'http://proxy-db.net',
    'IPPRIVACY': 'http://iprivacytools.com',
}
Detect_Tool_Site = 'http://www.iprivacytools.com/proxy-checker-anonymity-test/'
H_V_PATTERN = re.compile(r'HTTP_VIA: <span.*?>(.*?)</span>')
H_X_F_F_PATTERN = re.compile(r'HTTP_X_FORWARDED_FOR: <span.*?>(.*?)</span>')
Detect_Target = 'https://httpbin.org/get'
Proxy_Types = ['http', 'https', 'socks4', 'socks5']
LOCAL_IP_ADDR = '117.131.10.194'


# LOCAL_IP_ADDR = '140.206.71.62'


class ProxyModel(object):
    _database = Database()
    _client = Client()
    _db_reader = geo_db.Reader('./GeoLite2-City.mmdb')
    _doc_cache_size = 20
    _doc_to_remove_cache = {}
    _doc_to_update_cache = {}

    def __init__(self, doc_from_db=None):
        doc = doc_from_db if doc_from_db is not None else {}
        self.id = doc.get('_id', '')
        self.anonymity = doc.get('anonymity', 'unknown')
        self.ip_address = doc.get('ip_address', 'unknown')
        self.port = doc.get('port', -1)
        self.last_check_at = time.time() * 1000  # convert to ms
        self.location = doc.get('location', 'unknown, unknown')
        self.type = doc.get('type', 'unknown')
        self.available_sites = list()
        self.need_to_handle = True

    def proxy_str(self):
        return self.ip_address + ':' + str(self.port)

    def validate(self):
        """validate all requirements of proxy and save to db"""
        print('\x1b[1;34mHandling proxy %s \x1b[0m' % self)
        self.validate_type()
        if self.need_to_handle is True:
            self.validate_connection()
            self.anonymity = ProxyModel.detect_anonymity(self)
            self.location = ProxyModel.detect_location(self)
            ProxyModel._database.find_one_and_update({'_id': self.id}, self.to_json())
            print('\x1b[1;32mproxy %s saved \x1b[0m' % self)
        if len(ProxyModel._doc_to_remove_cache) >= ProxyModel._doc_cache_size:
            ProxyModel.flush_docs()

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
            except RequestException:
                continue
            except Exception as e:
                logging.error(e)
            else:
                available_sites.append(Connection_Validation_Targets[site])

        return {'sites': available_sites}

    @staticmethod
    def detect_anonymity(proxy):
        """evaluate the anonymity of proxy"""
        ProxyModel._client.set_proxies(proxy.proxy_str(), proxy.type)
        try:
            content = ProxyModel._client.get(Detect_Tool_Site)
        except RequestException:
            return 'unknown'
        except Exception as e:
            logging.error(e)
        else:
            if content is None:
                return 'unknown'
            via = re.search(H_V_PATTERN, content).groups()[0].strip()
            via_is_empty = via == 'anonymous / none'
            via_is_proxy = via == proxy.ip_address
            x_forwarded_for = re.search(H_X_F_F_PATTERN, content).groups()[0].strip()
            xff_is_empty = x_forwarded_for == 'anonymous / none'
            xff_is_proxy = x_forwarded_for == proxy.ip_address
            xff_is_lc = x_forwarded_for == LOCAL_IP_ADDR
            xff_is_rand = not xff_is_lc and not xff_is_proxy and not xff_is_empty
            if via_is_empty and xff_is_empty:
                return 'elite'
            if via_is_proxy and xff_is_rand:
                return 'distorting'
            if via_is_proxy and xff_is_proxy:
                return 'anonymous'
            if via_is_proxy and xff_is_lc:
                return 'transparent'
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
        types_to_try = [] if proxy.type == 'unknown' else [proxy.type]
        types_to_try.extend(Proxy_Types)
        for t in types_to_try:
            ProxyModel._client.set_proxies(proxy.proxy_str(), t)
            try:
                ProxyModel._client.get(Detect_Target)
            except RequestException as e:
                pass
            except Exception as e:
                logging.error(e)
            else:
                return {'action': 'update', 'type': t}
        print('\x1b[31mdrop %s \x1b[0m' % proxy.proxy_str())
        return {'action': 'remove'}

    @classmethod
    def flush_docs(cls):
        print('Flushing cache of document need to remove ... ')
        cls._database.remove({'_id': {'$in': list(cls._doc_to_remove_cache.values())}})
        cls._doc_to_remove_cache = {}
