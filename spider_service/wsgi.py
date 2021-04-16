# -*- coding:utf-8 -*-
from werkzeug.middleware.proxy_fix import ProxyFix

from app import createApp
import app.config as config

# production app server instance
app = createApp(config=config.ProdConfig)
app.wsgi_app = ProxyFix(app.wsgi_app)
