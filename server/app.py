from bottle import request, template, Bottle

app = Bottle(catchall=False)


@app.get('/hello/<name>')
def index(name):
    print('HTTP X FORWARDED FOR', request.environ.get('HTTP_X_FORWARDED_FOR'))
    print('REMOTE ADDR', request.environ.get('REMOTE_ADDR'))
    print('HTTP VIA', request.environ.get('HTTP_VIA'))
    return template('./index.html', name=name)


app.run(host='0.0.0.0', port=8080, reloader=True)
