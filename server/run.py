# -*- coding: utf-8 -*-
from proxy_server import app, bind_models, config

bind_models()
app.run_app(host=config['HOST'], port=config['PORT'], reloader=True)
