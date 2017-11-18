# -*- coding: utf-8 -*-
from bottle import Bottle, run

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


class BottleApp(object):
    def __init__(self, *args, **kwargs):
        self._app = Bottle(*args, **kwargs)

    @property
    def app(self):
        return self._app

    def hook_before_request(self, func):
        self._app.add_hook('before_request', func)

    def hook_after_request(self, func):
        self._app.add_hook('after_request', func)

    def middlewares(self, middlewares, options):
        self._app = middlewares(self._app, options)
        return self

    def routes(self, routes):
        for route in routes:
            self._app.route(route['path'], route['method'], route['handler'])

    def run_app(self, *args, **kwargs):
        run(self._app, *args, **kwargs)


app = BottleApp(catchall=True)
