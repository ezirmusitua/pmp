# -*- coding: utf-8 -*-
from bottle import Bottle, run

from proxy_server.route import routes


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

    def routes(self, _routes):
        for route in _routes:
            self._app.route(route['path'], route['method'], route['handler'])

    def run_app(self, *args, **kwargs):
        run(self._app, *args, **kwargs)


# bind_models()
# create bottle app
app = BottleApp(catchall=True)
# bind routes to app
app.routes(routes)
