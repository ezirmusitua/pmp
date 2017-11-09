import math
import logging
from bottle import request, template, Bottle, static_file, redirect, TEMPLATE_PATH, run
from beaker.middleware import SessionMiddleware
from utils import generate_pagination, validate_is_login, validate_not_login
from models.proxy import Proxy
from models.user import User
from models.tool import Tool, IpGeo, ip_geo_info_display_exporter

app = Bottle(catchall=True)
TEMPLATE_PATH.insert(0, 'templates')
SESSION_OPTIONS = {
    # 以文件的方式保存 session
    'session.type': 'file',
    # session 过期时间为 1d
    'session.cookie_expires': 24 * 60 * 60,
    # session 保存目录
    'session.data_dir': '.tmp/session',
    # 自动保存 session
    'session.auto': True
}


# reference: https://github.com/salimane/bottle-mvc/blob/master/project/controllers/static.py
@app.get('/static/<path:re:(.*?\.(js|css|ico))>')
def serve_static(path):
    return static_file(path, root='static')


@app.get('/login')
@app.post('/login')
def login():
    validate_is_login(request, redirect, '/')
    if request.method == 'POST':
        username = request.forms.username
        password = request.forms.password
        if User.validate(username, password):
            # get beaker.session in environ and update it
            sessions = request.environ.get('beaker.session')
            sessions['user'] = username
            sessions.save()
            redirect('/proxies')
        else:
            return template('templates/login.tpl', invalid=True)
    if request.method == 'GET':
        return template('templates/login.tpl', invalid=False)


@app.get('/')
@app.get('/proxies')
def proxy_list():
    validate_not_login(request, redirect)
    page_index = int(request.query.get('page-index', 1))
    page_return = Proxy.page(page_index - 1)
    pagination = generate_pagination(page_index, 10, page_return['count'])
    return template('templates/index.tpl', pagination=pagination, proxies=page_return['items'])


@app.get('/workers')
def worker_stats():
    validate_not_login(request, redirect)
    return template('templates/worker.tpl')


@app.get('/tools')
def proxy_tools():
    validate_not_login(request, redirect)
    tools = []
    ip_address = request.environ.get('REMOTE_ADDR')
    try:
        display = IpGeo.export(ip_address, ip_geo_info_display_exporter)
    except Exception as e:
        logging.error(e)
        tools.append(Tool('Ip Address Info: ', {'ip address: ': ip_address}))
    else:
        tools.append(Tool('Ip Address Info: ', display))
    return template('templates/tools.tpl', tools=tools)


app = SessionMiddleware(app, SESSION_OPTIONS)
run(app, host='127.0.0.1', port=8080, reloader=True)
