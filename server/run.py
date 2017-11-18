# -*- coding: utf-8 -*-
from proxy_server import app

app.run_app(host='127.0.0.1', port=8080, reloader=True)
