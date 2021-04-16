# -*- coding:utf-8 -*-
import datetime
import logging.config
import os
import time

from flask import Flask, send_from_directory, g, request, Response, Blueprint
from flask_restplus import Api, Namespace
from werkzeug.exceptions import default_exceptions, HTTPException
from werkzeug.utils import find_modules, import_string

from app import config
from app.extension import cors, schedule, redis, db
from app.utils import web_responsecode
from app.utils.web_response import WebResponse

log = logging.getLogger(__name__)

def createApp(config=config.BaseConfig):
    """Returns an initialized Flask application."""
    # This is a workaround for Alpine Linux (musl libc) quirk:
    # https://github.com/docker-library/python/issues/211
    import threading
    threading.stack_size(2 * 1024 * 1024)

    app = Flask(__name__)
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
            logpath = logdir + '/spider-proxy-' + '%s.log' % (today)

            logging.config.fileConfig(logfile, disable_existing_loggers=False, defaults={'logpath': logpath})
            logging.info('project logging setup already......')
    except Exception as e:
        print('cannot find config file logging.cfg')
        raise


def registerRouters(app: Flask):
    '''
    默认路由
    :param app:
    :return:
    '''

    # 默认路由
    @app.route('/')
    def index():
        responsemessage = {
            'get': u'get an useful proxy',
            'get_all': u'get all proxy from proxy pool',
            'delete?proxy=127.0.0.1:9001': u'delete an unable proxy',
            'get_status': u'proxy number'
        }
        jsonResponse = WebResponse(data=responsemessage)
        return jsonResponse.tojson()

    @app.route('/favicon.ico')
    def favicon():
        path = os.path.join(app.root_path, 'templates')
        return send_from_directory(path, 'favicon.png', mimetype='image/vnd.microsoft.icon')


    @app.before_request
    def before_request():
        g.start = time.time()
        g.request_time = lambda: '%.5fs' % (time.time() - g.start)
        log.info('请求信息:\n%s\n%s %s', request.full_path, request.headers, str(request.data, 'utf-8'))

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
    # bcrypt.init_app(app)
    cors.init_app(app)
    schedule.init_app(app)
    schedule.start()
    db.init_app(app)
    redis.init_app(app)



def registerBlueprints(app: Flask):
    '''
    配置蓝图
    :param app:
    :return:
    '''
    SECRET_KEY = app.config.get('SECRET_KEY', '11cfcdd982ee4964af7e94fa3488b218')
    url_prefix = app.config.get('BASE_PATH', '/')
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
    CONTROLLERS_MODULE_PATH = app.config.get('CONTROLLERS_PATH', 'app.controllers')

    blueprint = Blueprint('api', __name__,
                          url_prefix=url_prefix,
                          # static_url_path='core',
                          static_folder='static',
                          template_folder='templates')
    SWAGGER_API_VERSION = ''.join(SWAGGER_API_VERSION.split('.'))
    api = Api(blueprint, version=SWAGGER_API_VERSION,
              # doc='/core',
              security=SECRET_KEY,
              title=SWAGGER_TITLE,
              description=SWAGGER_DESCRIPTION,
              terms_url=SWAGGER_TERMS_URL,
              contact=SWAGGER_CONTACT,
              contact_url=SWAGGER_CONTACT_URL,
              contact_email=SWAGGER_CONTACT_EMAIL,
              license=SWAGGER_LICENSE,
              license_url=SWAGGER_LICENSE_URL)
    # 注册namespaces
    for name in find_modules(CONTROLLERS_MODULE_PATH, include_packages=False, recursive=True):
        log.info('导入的controller模块是: %s' % name)
        modname = import_string(name)
        for item in dir(modname):
            item = getattr(modname, item)
            if isinstance(item, Namespace):
                api.add_namespace(item)
    app.register_blueprint(blueprint)
    register_error_handlers(api)


def register_error_handlers(api: Api):
    '''
   配置异常处理
   :param app:
   :return:
   '''

    @api.errorhandler
    def error_handler(error):
        '''
        :param error: 对应下面的errr
        :return:
        '''
        ''' Catches all errors in the default_exceptions list '''
        msg = "Request resulted in {}".format(error)
        responsecode = web_responsecode.NOT_FOUND if isinstance(error,
                                                                HTTPException) else web_responsecode.INTERNAL_SERVER_ERROR
        responsemessage = getattr(error, 'message', msg)
        jsonResponse = WebResponse(responsecode, responsemessage)
        return jsonResponse.tojson()

    # for code in default_exceptions.keys():
    #     # 或者是requests.codes.INTERNAL_SERVER_ERROR
    #     app.register_error_handler(code, error_handler)
