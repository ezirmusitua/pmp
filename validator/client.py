# -*- coding: utf-8 -*-
import requests

Default_UA = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) ' \
             'Chrome/60.0.3112.113 Safari/537.36'
Default_Timeout = 2


class Client(object):
    def __init__(self, headers=None, proxies=None):
        self.headers = headers if headers is not None else {}
        self.headers['User-Agent'] = Default_UA
        self.proxies = proxies if proxies is not None else {}

    def get(self, url=None):
        if url is None:
            raise Exception('Need Url. ')
        response = requests.get(url, headers=self.headers, proxies=self.proxies, timeout=Default_Timeout)
        return response.text

    def set_proxies(self, proxy_str, ptype=None):
        self.proxies = {
            'http': (ptype if ptype is not None else 'http') + '://' + proxy_str,
            'https': (ptype if ptype is not None else 'https') + '://' + proxy_str,
        }

    def set_headers(self, headers):
        self.headers = headers

    def update_header(self, key, value):
        if self.headers is {}:
            self.headers = {}
        self.headers[key] = value

    def set_user_agent(self, ua_str):
        if self.headers is {}:
            self.headers = {}
        self.headers['User-Agent'] = ua_str


if __name__ == '__main__':
    client = Client()
    client.update_header('Debug', 'DebugString')
    assert (client.get('https://httpbin.org/get').find('DebugString') > -1)
    client.set_proxies('123.103.93.38:80')
    assert (client.get('https://httpbin.org/get').find('DebugString') > -1)
