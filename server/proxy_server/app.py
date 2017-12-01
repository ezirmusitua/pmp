# -*- coding: utf-8 -*-
from bottle import Bottle, run, TEMPLATE_PATH

TEMPLATE_PATH.insert(0, 'proxy_server')

from beaker.middleware import SessionMiddleware

from proxy_server import config
from proxy_server.route import routes

SESSION_OPTIONS = config['SESSION_OPTIONS']


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


# bind_models()
# create bottle app
app = BottleApp(catchall=True)
# bind routes to app
app.routes(routes)
# bind middlewares to app
app.middlewares(SessionMiddleware, SESSION_OPTIONS)
