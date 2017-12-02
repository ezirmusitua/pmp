# -*- coding: utf-8 -*-
from bottle import request

from proxy_server.models import Proxy


def check_user(username, password):
    from proxy_server import config
    admin = config['ADMIN']
    if username != admin['USERNAME'] or password != admin['PASSWORD']:
        return False
    return True


def check_token(token):
    return True


def get_random_proxy():
    check_token('')
    _type = request.query.get('type', '').split(',')
    connection = request.query.get('connection', '').split(',')
    anonymity = request.query.get('anonymity', '').split(',')
    size = request.query.get('size', None)
    is_shell = request.query.get('platform', '') == 'shell'
    proxy_strs = Proxy.search(_type, connection, anonymity, size)
    if is_shell:
        return proxy_strs[0] if len(proxy_strs) >= 1 else ''
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
