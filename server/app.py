from bottle import request, template, Bottle, static_file

app = Bottle(catchall=False)

# reference: https://github.com/salimane/bottle-mvc/blob/master/project/controllers/static.py
@app.get('/static/<path:re:(.*?\.(js|css|ico))>')
def serve_static(path):
    return static_file(path, root='static')


@app.get('/')
@app.get('/proxies')
@app.get('/proxies/')
def index():
    return template('templates/index.tpl', page=1)


@app.get('/proxies/<page:int>')
def proxy_list(page):
    return template('templates/index.tpl', page=page)


@app.get('/workers')
def worker_stats():
    return template('templates/worker.tpl')


@app.get('/tools')
def proxy_tools():
    return template('templates/tools.tpl')


app.run(host='0.0.0.0', port=8080, reloader=True)
