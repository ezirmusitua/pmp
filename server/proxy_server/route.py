# -*- coding: utf-8 -*-
from json import dumps
from bottle import request
from proxy_server.models import Proxy, Token


def check_user(username, password):
    from proxy_server import config
    admin = config['ADMIN']
    if username != admin['USERNAME'] or password != admin['PASSWORD']:
        return False
    return True


def check_token_key(key):
    return Token.validate(key)


def get_random_proxy():
    key = request.query.get('token-key', '')
    if not key: return dumps({'error': 'Token key is necessary'})
    if not check_token_key(key): return dumps({'error': 'Token key is invalid'})
    _type = request.query.get('type', '').split(',')
    connection = request.query.get('connection', '').split(',')
    anonymity = request.query.get('anonymity', '').split(',')
    size = request.query.get('size', None)
    is_shell = request.query.get('platform', '') == 'shell'
    proxy_strs = Proxy.search(_type, connection, anonymity, size)
    if is_shell:
        return proxy_strs[0] if len(proxy_strs) >= 1 else ''
    return dumps({
        'count': len(proxy_strs),
        'items': proxy_strs,
        'type': _type,
        'connection': connection,
        'anonymity': anonymity,
        'size': size
    })


def operate_token_route(operation):
    def route():
        username = request.query.get('username')
        password = request.query.get('password')
        if not check_user(username, password):
            return dumps({'error': 'Invalid User'})
        key = request.query.get('key', None)
        if not key:
            return dumps({'error': 'key in query is necessary'})
        if operation == 'POST':
            token = Token.generate(key)
            return dumps({'status': 'success', 'token': token})
        if operation == 'DELETE':
            Token.delete(key)
            return dumps({'status': 'success'})

    return route


routes = [{
    'path': '/lucky-proxy',
    'method': 'GET',
    'handler': get_random_proxy,
}, {
    'path': '/token',
    'method': 'POST',
    'handler': operate_token_route('POST')
}, {
    'path': '/token',
    'method': 'DELETE',
    'handler': operate_token_route('DELETE')
}]
