# -*- coding:utf-8 -*-
from app import createApp
import app.config as config

app = createApp(config=config.DevConfig)

# if __name__ == '__main__':
#     '''Testing environment startup script'''
#     app.debug = True
#     port = app.config.get('PORT', 9000)
#     app.run(host='0.0.0.0', port=port)
