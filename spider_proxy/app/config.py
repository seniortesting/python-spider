# -*- coding:utf-8 -*-
import os


class BaseConfig(object):
    '''default configuration'''
    BASE_PATH = ''
    PORT = 9001
    JSON_AS_ASCII = False  # 这里需要用到jsontify的时候才会返回中文,如果直接是中文字符,返回的还是乱码
    SECRET_KEY = os.environ.get('SECRET_KEY') or '2fed9235eb984bf3b9de74e305f20b7e'
    # Swagger
    SWAGGER_API_VERSION = '1.0'
    SWAGGER_TITLE = '代理IP池接口'  # 眼值开放数据接口文档
    SWAGGER_DESCRIPTION = "代理IP池开放数据接口文档"  #
    SWAGGER_TERMS_URL = 'https://open.pingbook.top/proxy'
    SWAGGER_CONTACT = 'Walter Hu'
    SWAGGER_CONTACT_URL = 'https://open.pingbook.top/proxy'
    SWAGGER_CONTACT_EMAIL = 'alterhu2020@gmail.com'
    SWAGGER_LICENSE = 'MIT'
    SWAGGER_LICENSE_URL = 'https://open.pingbook.top/proxy'
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
    SCHEDULER_JOBSTORES = None
    SCHEDULER_EXECUTORS = None
    SCHEDULER_JOB_DEFAULTS = None
    SCHEDULER_TIMEZONE = None
    SCHEDULER_API_ENABLED = True
    SCHEDULER_API_PREFIX = BASE_PATH + '/scheduler'
    SCHEDULER_ENDPOINT_PREFIX = None
    JOBS = [
        {
            'id': 'fetch_proxy',
            'name': '抓取代理任务',
            'func': 'app.jobs.proxy_fetch_job:FetchJob',
            'trigger': 'interval',  # 可选择参数:interval,cron, apscheduler.schedulers.base.BaseScheduler#add_job
            'seconds': 100
        },
        {
            'id': 'verify_proxy',
            'name': '验证代理任务',
            'func': 'app.jobs.proxy_check_raw:checkRawProxyJob',
            'trigger': 'interval',  # 可选择参数:interval,cron, apscheduler.schedulers.base.BaseScheduler#add_job
            'seconds': 60
        },
        {
            'id': 'verify_proxy_2',
            'name': '二次验证代理任务',
            'func': 'app.jobs.proxy_check_valid:checkValidProxyJob',
            'trigger': 'interval',  # 可选择参数:interval,cron, apscheduler.schedulers.base.BaseScheduler#add_job
            'seconds': 65
        }
    ]


class DevConfig(BaseConfig):
    '''developement configuration'''
    TESTING = True
    DEBUG = True
    # 日志目录
    LOGGING_FOLDER = "D:\\logs"
    # 上传配置
    UPLOAD_FOLDER = "D:\\uploads"
    # mysql配置
    DATA_STORE_TYPE='mysql'
    # SQLALCHEMY配置
    SQLALCHEMY_ECHO = True
    SQL_SERVER_NAME = '127.0.0.1'
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://syscorer:s6s@#@!L0ngh@{0}:3306/heap_stack'.format(SQL_SERVER_NAME)
    # 配置多个数据库源头
    SQLALCHEMY_BINDS = {
        "slave1": 'mysql+pymysql://syscorer:s6s@#@!L0ngh@{0}:3306/heap_stack'.format(SQL_SERVER_NAME)
    }
    # Redis配置
    REDIS_HOST = '192.168.1.103'
    REDIS_URL = "redis://:5aebda6b0403478fbd5e748991455b33@{0}:6379/5".format(REDIS_HOST)


class ProdConfig(BaseConfig):
    '''production configuration'''
    # 日志目录
    LOGGING_FOLDER = "/logs"
    # 上传配置
    UPLOAD_FOLDER = "/uploads"
    # mysql配置
    DATA_STORE_TYPE='mysql'
    # SQLALCHEMY配置
    SQLALCHEMY_ECHO = True
    SQL_SERVER_NAME = '127.0.0.1'
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://syscorer:s6s@#@!L0ngh@{0}:3306/heap_stack'.format(SQL_SERVER_NAME)
    # 配置多个数据库源头
    SQLALCHEMY_BINDS = {
        "slave1": 'mysql+pymysql://syscorer:s6s@#@!L0ngh@{0}:3306/heap_stack'.format(SQL_SERVER_NAME)
    }
    # Redis配置
    # REDIS_HOST ='127.0.0.1'
    REDIS_HOST = '172.16.51.174'
    REDIS_URL = "redis://:5aebda6b0403478fbd5e748991455b33@{0}:6379/5".format(REDIS_HOST)
