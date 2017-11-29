# -*- coding: utf-8 -*-
import os

from ProxyGeoDetector import Detector

from .client import Client
from .chain import Handler, RChain
from .proxy import ProxyToUpdatePool

Connection_Detect_Targets = {
    'httpbin': 'https://httpbin.org',
    'google': 'https://www.google.com',
    'baidu': 'https://baidu.com',
    'cn-proxy': 'http://cn-proxy.com',
    'premproxy': 'https://premproxy.com',
    'proxydb': 'http://proxy-db.net',
}
Proxy_Types = ['http', 'https', 'socks4', 'socks5']
Proxy_Type_Detect_Url = 'https://httpbin.org'
Request_Anonymity_Headers_Detect_Url = 'https://jferroal/proxy/anonymity-checker'


def validate_usability(proxy):
    client = Client()
    client.set_proxies(proxy.proxy_str(), proxy.proxy_type[0])
    is_usable = 0
    for site in ['baidu', 'google']:
        try:
            client.get(Connection_Detect_Targets[site])
        except Exception:
            is_usable += 0
        else:
            is_usable += 1
    if is_usable == 0:
        return True
    return False


def validate_connection(proxy):
    available_sites = list()
    client = Client()
    client.set_proxies(proxy.proxy_str(), proxy.proxy_type[0])
    for site in Connection_Detect_Targets:
        try:
            client.get(Connection_Detect_Targets[site])
        except Exception:
            continue
        else:
            available_sites.append(site)
    return available_sites


def validate_anonymity(proxy):
    client = Client()
    client.set_proxies(proxy.proxy_str(), proxy.proxy_type[0])
    anonymity = ['unknown']
    try:
        # FIXME: Update here after server done
        # anonymity = client.get(Request_Anonymity_Headers_Detect_Url).json()
        anonymity = ['unknown']
    except Exception:
        return anonymity
    else:
        return anonymity


def validate_location(proxy):
    db_path = os.path.split(os.path.realpath(__file__))[0] + '/GeoLite2-City.mmdb'
    return Detector.open_reader(db_path)(proxy.ip_address).location_label()


def validate_proxy_type(proxy):
    client = Client()
    proxy_type = ['http']
    for t in Proxy_Types:
        client.set_proxies(proxy.proxy_str(), t)
        try:
            client.get(Proxy_Type_Detect_Url)
        except Exception:
            continue
        else:
            proxy_type.append(t)
    return proxy_type


def drop_or_save(proxy):
    proxy_pool = ProxyToUpdatePool()
    proxy_pool.add_to_pool(proxy)
    proxy_pool.handle_pool()


validation_chain = RChain() \
    .append_handler(Handler('proxy_type', validate_proxy_type)) \
    .append_handler(Handler('invalid', validate_usability)) \
    .append_handler(Handler('connection', validate_connection)) \
    .append_handler(Handler('anonymity', validate_anonymity)) \
    .append_handler(Handler('location', validate_location)) \
    .append_handler(Handler('db', drop_or_save))
