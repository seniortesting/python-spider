# -*- coding:utf-8 -*-
from flask_apscheduler import APScheduler
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy

# 跨域访问
from flask_redis import FlaskRedis

cors = CORS()
# mysql 服务器
db =SQLAlchemy()
# redis服务器
redis = FlaskRedis()
# 定时任务
schedule= APScheduler()
