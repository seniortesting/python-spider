# -*- coding:utf-8 -*-

# production app server instance
from werkzeug.middleware.proxy_fix import ProxyFix

from app import createApp, config

app = createApp(config=config.ProdConfig)
app.wsgi_app = ProxyFix(app.wsgi_app)
