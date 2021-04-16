# -*- coding:utf-8 -*-
import os


class BaseConfig(object):
    '''default configuration'''
    BASE_PATH = '/'
    PORT = 9000
    JSON_AS_ASCII = False  # 这里需要用到jsontify的时候才会返回中文,如果直接是中文字符,返回的还是乱码
    SECRET_KEY = os.environ.get('SECRET_KEY') or '2fed9235eb984bf3b9de74e305f20b7e'
    # Swagger
    SWAGGER_API_VERSION = '1.0'
    SWAGGER_TITLE = '开放API接口'  # 眼值开放数据接口文档
    SWAGGER_DESCRIPTION = "开放数据接口文档"  #
    SWAGGER_TERMS_URL = 'https://pingbook.top'
    SWAGGER_CONTACT = 'Walter Hu'
    SWAGGER_CONTACT_URL = 'https://pingbook.top'
    SWAGGER_CONTACT_EMAIL = 'alterhu2020@gmail.com'
    SWAGGER_LICENSE = 'MIT'
    SWAGGER_LICENSE_URL = 'https://pingbook.top'
    # SQLALCHEMY配置
    SQLALCHEMY_COMMIT_ON_TEARDOWN = True
    SQLALCHEMY_RECORD_QUERIES = True
    # show variables like 'max_connections';
    SQLALCHEMY_POOL_SIZE = 30
    # MariaDB is configured to have a 600 second timeout
    SQLALCHEMY_POOL_TIMEOUT = 80
    # 查看timeout 时间 ： show global variables like '%timeout%'; 该值必须小于数据库服务器的interactive_timeout
    # 查看对应的最大连接池,需要小于默认的8小时28800：
    SQLALCHEMY_POOL_RECYCLE = 80
    SQLALCHEMY_MAX_OVERFLOW = 100
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # 定时任务相关：参考文件： C:/Users/Walter/.virtualenvs/Flask-Crawler-VyEMoroi/Lib/site-packages/flask_apscheduler/scheduler.py:292
    # SCHEDULER_JOBSTORES=None
    # SCHEDULER_EXECUTORS=None
    # SCHEDULER_JOB_DEFAULTS=None
    # SCHEDULER_TIMEZONE=None
    SCHEDULER_API_ENABLED = True
    SCHEDULER_API_PREFIX = '/scheduler'
    # SCHEDULER_ENDPOINT_PREFIX=None


class DevConfig(BaseConfig):
    '''developement configuration'''
    TESTING = True
    DEBUG = True
    # 日志目录
    LOGGING_FOLDER = "D:\\logs"
    # 上传配置
    UPLOAD_FOLDER = "D:\\uploads"
    # SQLALCHEMY配置
    SQLALCHEMY_ECHO = True
    SQL_SERVER_IP = '127.0.0.1'
    SQL_SERVER_PORT = 3306
    SQL_SERVER_USERNAME = 'syscorer'
    SQL_SERVER_PASSWORD = 's6s@#@!L0ngh'
    SQL_SERVER_DATABASE = 'jvfast'
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://{0}:{1}@{2}:{3}/{4}'.format(SQL_SERVER_USERNAME, SQL_SERVER_PASSWORD,
                                                                           SQL_SERVER_IP, SQL_SERVER_PORT,
                                                                           SQL_SERVER_DATABASE)
    # 配置多个数据库源头
    SQLALCHEMY_BINDS = {
        "slave1": 'mysql+pymysql://{0}:{1}@{2}:{3}/{4}'.format(SQL_SERVER_USERNAME, SQL_SERVER_PASSWORD,
                                                               SQL_SERVER_IP, SQL_SERVER_PORT,
                                                               SQL_SERVER_DATABASE)
    }
    # 获取代理请求的地址
    PROXY_URL = 'http://{}:9001/proxy/get'.format(SQL_SERVER_IP)


class ProdConfig(BaseConfig):
    '''production configuration'''
    # 日志目录
    LOGGING_FOLDER = "/logs"
    # 上传配置
    UPLOAD_FOLDER = "/uploads"
    # SQLALCHEMY配置
    SQLALCHEMY_ECHO = True
    SQL_SERVER_IP = '127.0.0.1'
    SQL_SERVER_PORT = 3306
    SQL_SERVER_USERNAME = 'syscorer'
    SQL_SERVER_PASSWORD = 's6s@#@!L0ngh'
    SQL_SERVER_DATABASE = 'jvfast'
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://{0}:{1}@{2}:{3}/{4}'.format(SQL_SERVER_USERNAME, SQL_SERVER_PASSWORD,
                                                                           SQL_SERVER_IP, SQL_SERVER_PORT,
                                                                           SQL_SERVER_DATABASE)
    SQLALCHEMY_BINDS = {
        "slave1": 'mysql+pymysql://{0}:{1}@{2}:{3}/{4}'.format(SQL_SERVER_USERNAME, SQL_SERVER_PASSWORD,
                                                               SQL_SERVER_IP, SQL_SERVER_PORT,
                                                               SQL_SERVER_DATABASE)
    }
    # 获取代理请求的地址
    PROXY_URL = 'https://{}/proxy/get'.format(SQL_SERVER_IP)
