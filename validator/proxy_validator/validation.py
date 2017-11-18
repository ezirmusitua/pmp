# -*- coding: utf-8 -*-
import os

from getIpGeoInfo import IpGeo

from proxy_validator.client import Client
from proxy_validator.chain import Handler, RChain
from proxy_validator.proxy import ProxyToUpdatePool

Connection_Detect_Targets = {
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
Proxy_Types = ['http', 'https', 'socks4', 'socks5']
Proxy_Type_Detect_Url = 'https://httpbin.org'
Request_Anonymity_Headers_Detect_Url = 'https://jferroal/proxy/anonymity-checker'


def validate_connection(proxy):
    available_sites = list()
    client = Client()
    client.set_proxies(proxy.proxy_str(), proxy.proxy_types[0])
    for site in Connection_Detect_Targets:
        try:
            client.get(Connection_Detect_Targets[site])
        except Exception as e:
            print(e)
        else:
            available_sites.append(site)
    return available_sites


def validate_anonymity(proxy):
    client = Client()
    client.set_proxies(proxy.proxy_str(), proxy.type)
    anonymity = ['unknown']
    try:
        anonymity = client.get(Request_Anonymity_Headers_Detect_Url).json()
    except Exception as e:
        print(e)
        return anonymity
    else:
        return anonymity


def validate_location(proxy):
    db_path = os.path.split(os.path.realpath(__file__))[0] + '/GeoLite2-City.mmdb'
    return IpGeo.open_reader(db_path)(proxy.ip_address).location_label()


def validate_proxy_type(proxy):
    client = Client()
    proxy_types = list()
    for t in Proxy_Types:
        client.set_proxies(proxy.proxy_str(), t)
        try:
            client.get(Proxy_Type_Detect_Url)
        except Exception as e:
            print(e)
        else:
            proxy_types.append(t)
    return proxy_types


def drop_or_save(proxy):
    proxy_pool = ProxyToUpdatePool()
    proxy_pool.handle_pool()
    proxy_pool.add_to_pool(proxy)


validation_chain = RChain() \
    .append_handler(Handler('proxy_type', validate_location)) \
    .append_handler(Handler('connection', validate_connection)) \
    .append_handler(Handler('anonymity', validate_anonymity)) \
    .append_handler(Handler('location', validate_location)) \
    .append_handler(Handler('db', drop_or_save))
