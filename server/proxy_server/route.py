# -*- coding: utf-8 -*-
from bottle import request, template, static_file, redirect

from proxy_server.models import Proxy, User
from proxy_server.utils import generate_pagination, login_required


# reference: https://github.com/salimane/bottle-mvc/blob/master/project/controllers/static.py
def serve_static(path):
    return static_file(path, root='proxy_server/static')


def login():
    sessions = request.environ.get('beaker.session')
    if sessions.get('user') is not None:
        redirect('/')
    if request.method == 'POST':
        username = request.forms.username
        password = request.forms.password
        if User.validate(username, password):
            sessions['user'] = username
            sessions.save()
            redirect('/proxies')
        else:
            return template('templates/login.tpl', invalid=True)
    if request.method == 'GET':
        return template('templates/login.tpl', invalid=False)


def proxy_list():
    login_required()
    page_index = int(request.query.get('page-index', 1))
    page_return = Proxy.page(page_index - 1)
    pagination = generate_pagination(page_index, 10, page_return['count'])
    return template('templates/index.tpl', pagination=pagination, proxies=page_return['items'])


def export_proxies():
    login_required()
    proxies = Proxy.list_all()['items']
    return template('templates/export.tpl', proxies=map(lambda p: p.to_csv(), proxies))


routes = [{
    'path': '/proxy_server/static/<path:re:(.*?\.(js|css|ico))>',
    'method': 'GET',
    'handler': serve_static
}, {
    'path': '/login',
    'method': 'GET',
    'handler': login,
}, {
    'path': '/login',
    'method': 'POST',
    'handler': login,
}, {
    'path': '/',
    'method': 'GET',
    'handler': proxy_list,
}, {
    'path': '/proxies',
    'method': 'GET',
    'handler': proxy_list,
}, {
    'path': '/export',
    'method': 'GET',
    'handler': export_proxies
}]
