import math
from bottle import request, template, Bottle, static_file
from models.proxy import Proxy
from utils import generate_pagination

app = Bottle(catchall=False)


# reference: https://github.com/salimane/bottle-mvc/blob/master/project/controllers/static.py
@app.get('/static/<path:re:(.*?\.(js|css|ico))>')
def serve_static(path):
    return static_file(path, root='static')


@app.get('/')
@app.get('/proxies')
def proxy_list():
    page_index = int(request.query.get('page-index', 1))
    page_return = Proxy.page(page_index - 1)
    pagination = generate_pagination(page_index, 10, page_return['count'])
    print('hello world')
    return template('templates/index.tpl', pagination=pagination, proxies=page_return['items'])


@app.get('/workers')
def worker_stats():
    return template('templates/worker.tpl')


@app.get('/tools')
def proxy_tools():
    return template('templates/tools.tpl')


app.run(host='127.0.0.1', port=8080, reloader=True)
