from bottle import request, template, Bottle

app = Bottle(catchall=False)


@app.get('/')
@app.get('/proxy-list')
def index():
    return template('templates/index.tpl', page=1)


@app.get('/proxy-list/<page:int>')
def index(page):
    return template('templates/index.tpl', page=page)


app.run(host='0.0.0.0', port=8080, reloader=True)
