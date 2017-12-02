# -*- coding: utf-8 -*-
from bottle import request

from proxy_server.models import Proxy


def check_token():
    return True


def get_random_proxy():
    check_token()
    _type = request.query.get('type', '').split(',')
    connection = request.query.get('connection', '').split(',')
    anonymity = request.query.get('anonymity', '').split(',')
    size = request.query.get('size', None)
    proxy_strs = Proxy.search(_type, connection, anonymity, size)
    from json import dumps
    return dumps({
        'count': len(proxy_strs),
        'items': proxy_strs,
        'type': _type,
        'connection': connection,
        'anonymity': anonymity,
        'size': size
    })


routes = [{
    'path': '/lucky-proxy',
    'method': 'GET',
    'handler': get_random_proxy,
}, {
    'path': 'token',
    'method': 'POST',
    'handler': lambda x: x
}]
