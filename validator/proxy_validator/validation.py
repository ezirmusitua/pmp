# -*- coding: utf-8 -*-
import os
import logging
from ProxyGeoDetector import Detector

from proxy_validator import config
from proxy_validator.chain import Handler, RChain
from proxy_validator.client import Client

Connection_Detect_Targets = config['CONNECTION_DETECT_TARGETS']
Proxy_Types = config['PROXY_TYPES']
Proxy_Type_Detect_Url = config['TYPE_DETECT_URL']
Anonymity_Detect_Url = config['ANONYMITY_DETECT_URL']


def validate_usability(proxy):
    client = Client()
    client.set_proxies(proxy.proxy_str(), proxy.proxy_type[0])
    is_usable = 0
    for site in ['baidu', 'google']:
        try:
            client.get(Connection_Detect_Targets[site])
        except Exception as e:
            logging.warning(e)
            is_usable += 0
        else:
            is_usable += 1
    if is_usable == 0:
        return True
    return False


def validate_connection(proxy):
    if proxy.invalid: return []
    available_sites = list()
    client = Client()
    client.set_proxies(proxy.proxy_str(), proxy.proxy_type[0])
    for site in Connection_Detect_Targets:
        try:
            client.get(Connection_Detect_Targets[site])
        except Exception as e:
            logging.warning(e)
            continue
        else:
            available_sites.append(site)
    return available_sites


def validate_anonymity(proxy):
    if proxy.invalid: return []
    client = Client()
    client.set_proxies(proxy.proxy_str(), proxy.proxy_type[0])
    anonymity = ['unknown']
    try:
        if Anonymity_Detect_Url:
            anonymity = client.get(Anonymity_Detect_Url).json()
    except Exception as e:
        logging.warning(e)
        return anonymity
    else:
        return anonymity


def validate_location(proxy):
    if proxy.invalid: return []
    db_path = os.path.split(os.path.realpath(__file__))[0] + '/GeoLite2-City.mmdb'
    # FIXME: update geo detector default locale
    return Detector.open_reader(db_path)(proxy.ip_address, None).location_label()


def validate_proxy_type(proxy):
    if proxy.invalid: return []
    client = Client()
    proxy_type = ['http']
    for t in Proxy_Types:
        client.set_proxies(proxy.proxy_str(), t)
        try:
            client.get(Proxy_Type_Detect_Url)
        except Exception as e:
            logging.warning(e)
            continue
        else:
            proxy_type.append(t)
    return proxy_type


def save_or_remove(proxy):
    import time
    proxy.save_or_remove()
    return time.time()


validation_chain = RChain() \
    .append_handler(Handler('proxy_type', validate_proxy_type)) \
    .append_handler(Handler('invalid', validate_usability)) \
    .append_handler(Handler('connection', validate_connection)) \
    .append_handler(Handler('anonymity', validate_anonymity)) \
    .append_handler(Handler('location', validate_location)) \
    .append_handler(Handler('last_check_at', save_or_remove))
