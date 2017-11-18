# -*- coding: utf-8 -*-
from bottle import TEMPLATE_PATH
from beaker.middleware import SessionMiddleware

from app import app
from route import routes

TEMPLATE_PATH.insert(0, 'templates')
app.routes(routes)
app.middlewares(SessionMiddleware, {
    # 以文件的方式保存 session
    'session.type': 'file',
    # session 过期时间为 1d
    'session.cookie_expires': 24 * 60 * 60,
    # session 保存目录
    'session.data_dir': '.tmp/session',
    # 自动保存 session
    'session.auto': True
})

app.run_app(host='127.0.0.1', port=8080, reloader=True)
