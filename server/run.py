# -*- coding: utf-8 -*-
from proxy_server import app, bind_models

bind_models()
app.run_app(host='127.0.0.1', port=8080, reloader=True)
