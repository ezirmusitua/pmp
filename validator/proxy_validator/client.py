# -*- coding: utf-8 -*-
import requests

Default_UA = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) ' \
             'Chrome/60.0.3112.113 Safari/537.36'
Default_Timeout = 1


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

    def set_proxies(self, proxy_str, ptype=None):
        self.proxies = {
            'http': (ptype if ptype is not None else 'http') + '://' + proxy_str,
            'https': (ptype if ptype is not None else 'https') + '://' + proxy_str,
        }
