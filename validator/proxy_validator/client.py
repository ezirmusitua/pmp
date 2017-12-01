# -*- coding: utf-8 -*-
import requests
from proxy_validator import config

Default_UA = config['CLIENT_UA']
Default_Timeout = config['CLIENT_TIMEOUT']


class Client(object):
    def __init__(self, headers=None, proxies=None):
        self.headers = headers if headers is not None else {}
        self.headers['User-Agent'] = Default_UA
        self.proxies = proxies if proxies is not None else {}
        self.session = requests.Session()

    def get(self, url=None):
        if url is None:
            raise Exception('Need Url. ')
        response = self.session.get(url, headers=self.headers, proxies=self.proxies, timeout=Default_Timeout)
        if response.status_code != 200:
            return None
        return response.text

    def set_proxies(self, proxy_str, ptype='http'):
        self.proxies = {
            'http': (ptype if ptype is not None else 'http') + '://' + proxy_str,
            'https': (ptype if ptype is not None else 'https') + '://' + proxy_str,
        }
