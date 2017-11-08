import math
from bottle import request, template, Bottle, static_file, redirect
from models.proxy import Proxy
from utils import generate_pagination

app = Bottle(catchall=False)


# reference: https://github.com/salimane/bottle-mvc/blob/master/project/controllers/static.py
@app.get('/static/<path:re:(.*?\.(js|css|ico))>')
def serve_static(path):
    return static_file(path, root='static')

@app.get('/login')
@app.post('/login')
def login():
    if request.method == 'POST':
        username = request.forms.username
        password = request.forms.password
        # TODO: Create User Model 
        # TODO: Init admin user
        if username == 'jferroal' and password == '123123':
            print('Go Here')
            redirect('/proxies')
        else:
            return template('templates/login.tpl')
    if request.method == 'GET':
        return template('templates/login.tpl')




@app.get('/')
@app.get('/proxies')
def proxy_list():
    page_index = int(request.query.get('page-index', 1))
    page_return = Proxy.page(page_index - 1)
    pagination = generate_pagination(page_index, 10, page_return['count'])
    return template('templates/index.tpl', pagination=pagination, proxies=page_return['items'])


app.run(host='127.0.0.1', port=8080, reloader=True)
