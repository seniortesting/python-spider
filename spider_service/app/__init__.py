# -*- coding:utf-8 -*-
import datetime
import logging.config
import os
import time

from flask import Flask, send_from_directory, g, request, Response, jsonify
from flask_restx import Namespace, Api
from werkzeug.exceptions import HTTPException, default_exceptions
from werkzeug.utils import find_modules, import_string

from app import config
from app.extension import db, bcrypt, cors
from app.api.util.web_responsecode import WebResponseCode

log = logging.getLogger(__name__)
"""Returns an initialized Flask application."""
# This is a workaround for Alpine Linux (musl libc) quirk:
# https://github.com/docker-library/python/issues/211
import threading

threading.stack_size(2 * 1024 * 1024)
app = Flask(__name__)


def createApp(config=config.BaseConfig):
    app.config.from_object(config)
    setupLogging(app)
    registerRouters(app)
    registerExtensions(app)
    registerBlueprints(app)

    return app


def setupLogging(app: Flask):
    '''
    配置日志
    :param app:
    :return:
    '''
    try:
        logfile = os.path.join(os.path.dirname(__file__), 'logging.cfg')
        existfile = os.path.exists(logfile)
        if existfile:
            logdir = app.config.get('LOGGING_FOLDER')
            if not os.path.exists(logdir):
                os.makedirs(logdir)
            today = datetime.date.today().strftime('%Y-%m-%d')
            logpath = logdir + '/service-spider-' + '%s.log' % (today)

            logging.config.fileConfig(logfile, disable_existing_loggers=False, defaults={'logpath': logpath})
            logging.info('project logging setup already......')
    except Exception as e:
        print('cannot find config file logging.cfg')
        raise


def registerRouters(app: Flask):
    @app.route('/favicon.ico')
    def favicon():
        path = os.path.join(app.root_path, 'templates')
        return send_from_directory(path, 'favicon.png', mimetype='image/vnd.microsoft.icon')

    @app.before_request
    def before_request():
        g.start = time.time()
        g.request_time = lambda: '%.5fs' % (time.time() - g.start)
        log.info('请求信息,地址是: %s\n%s %s', request.full_path, request.headers, str(request.data, 'utf-8'))

    @app.after_request
    def after_request(response: Response):
        # http://werkzeug.pocoo.org/docs/0.14/wrappers/#werkzeug.wrappers.BaseResponse.get_data
        # try:
        #     log.info('数据返回Response信息:\n%s %s ', response.headers, str(response.data, 'utf-8'))
        # except Exception as e:
        #     log.error('打印Response日志内容出错!')
        # if (response.response and response.status_code == 200):
        # response.response[0] = response.response[0].replace('__EXECUTION_TIME__', str(diff))
        # response.headers["content-length"] = len(response.response[0])
        response.headers["X-Content-Type-Options"] = "nosniff"
        response.headers["X-Frame-Options"] = "deny"
        return response


def registerExtensions(app: Flask):
    '''
    配置插件
    :param app:
    :return:
    '''
    bcrypt.init_app(app)
    cors.init_app(app)
    # schedule.init_app(app)
    # schedule.start()
    db.init_app(app)


def registerBlueprints(app: Flask):
    '''
    配置蓝图
    :param app:
    :return:
    '''
    SECRET_KEY = app.config.get('SECRET_KEY', '11cfcdd982ee4964af7e94fa3488b218')
    BASE_PATH = app.config.get('BASE_PATH', '/')
    # Swagger 配置
    SWAGGER_API_VERSION = app.config.get('SWAGGER_API_VERSION', '1.0')
    SWAGGER_TITLE = app.config.get('SWAGGER_TITLE', 'Swagger API')
    SWAGGER_DESCRIPTION = app.config.get('SWAGGER_DESCRIPTION', 'API Document specifications')
    SWAGGER_TERMS_URL = app.config.get('SWAGGER_TERMS_URL', 'https://pingbook.top')
    SWAGGER_CONTACT = app.config.get('SWAGGER_CONTACT', '<pingbook.top> alterhu2020@gmail.com')
    SWAGGER_CONTACT_URL = app.config.get('SWAGGER_CONTACT_URL', 'https://pingbook.top')
    SWAGGER_CONTACT_EMAIL = app.config.get('SWAGGER_CONTACT_EMAIL', '<pingbook.top> alterhu2020@gmail.com')
    SWAGGER_LICENSE = app.config.get('SWAGGER_LICENSE', 'MIT')
    SWAGGER_LICENSE_URL = app.config.get('SWAGGER_LICENSE_URL', 'https://pingbook.top')
    # controller路径
    CONTROLLERS_MODULE_PATH = app.config.get('CONTROLLERS_PATH', 'app.api.controller')
    SWAGGER_API_VERSION = ''.join(SWAGGER_API_VERSION.split('.'))

    # blueprint = Blueprint('api', __name__,
    #                       url_prefix=url_prefix,
    #                       # static_url_path='core',
    #                       static_folder='static',
    #                       template_folder='templates')
    # flask-restplus对应的api接口
    api = Api(version=SWAGGER_API_VERSION,
              doc=BASE_PATH,
              security=SECRET_KEY,
              title=SWAGGER_TITLE,
              description=SWAGGER_DESCRIPTION,
              terms_url=SWAGGER_TERMS_URL,
              contact=SWAGGER_CONTACT,
              contact_url=SWAGGER_CONTACT_URL,
              contact_email=SWAGGER_CONTACT_EMAIL,
              license=SWAGGER_LICENSE,
              license_url=SWAGGER_LICENSE_URL)
    api.init_app(app)
    # 注册namespaces
    for name in find_modules(CONTROLLERS_MODULE_PATH, include_packages=False, recursive=True):
        log.info('导入的controller模块是: %s' % name)
        modname = import_string(name)
        for item in dir(modname):
            item = getattr(modname, item)
            if isinstance(item, Namespace):
                api.add_namespace(item)

    def default_error_handler(error):
        '''
           :param error: 对应下面的errr
           :return:
           '''
        msg = "WebRequest resulted in {}".format(error)
        log.exception(error, exc_info=True)
        responsecode = WebResponseCode.NOT_FOUND if isinstance(error,
                                                               HTTPException) else WebResponseCode.INTERNAL_SERVER_ERROR
        responsemessage = getattr(error, 'message', msg)
        response = {
            'code': responsecode.code,
            'msg': responsemessage,
            'request_time': datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        }
        with app.app_context():
            return jsonify(response)

    for code in default_exceptions.keys():
        ex = default_exceptions.get(code)
        app.register_error_handler(ex, default_error_handler)

    # app.register_blueprint(blueprint)
