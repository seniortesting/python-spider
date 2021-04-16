# -*- coding:utf-8 -*-
from flask_apscheduler import APScheduler
from flask_bcrypt import Bcrypt
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_jwt_extended import JWTManager
from flask_marshmallow import Marshmallow

# 加密算法
bcrypt = Bcrypt()
# 跨域访问
cors = CORS()
# 数据库设置
db =SQLAlchemy()
# 定时任务
# schedule= APScheduler()
migrate = Migrate()
jwt = JWTManager()
ma = Marshmallow()
