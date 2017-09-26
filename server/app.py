from bottle import request, template, Bottle

app = Bottle(catchall=False)


@app.get('/')
@app.get('/list')
@app.get('/list/')
def index():
    return template('templates/index.tpl', page=1)


@app.get('/list/<page:int>')
def proxy_list(page):
    return template('templates/index.tpl', page=page)


@app.get('/stats')
def worker_stats():
    return template('templates/stats.tpl')


app.run(host='0.0.0.0', port=8080, reloader=True)
