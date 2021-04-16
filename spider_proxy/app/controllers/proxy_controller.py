# -*- coding:utf-8 -*-
import json
import logging
import random

from flask import current_app, request
from flask_restplus import Namespace
from sqlalchemy import desc

from app import jobs, WebResponse
from app.models.models import ProxyValid, ProxyRaw
from app.models.proxy import Proxy
from app.utils.base_resource import BaseResource
from app.utils.db.redis_helper import RedisHelper
from app.utils.web_responsecode import WebResponseCode
from app.extension import db as sql

log = logging.getLogger(__name__)
nsproxy = Namespace('', description='代理接口')


@nsproxy.route("/get")
class ProxyGetController(BaseResource):
    def get(self):
        '''
        请求样例: /get
                 /get?type=valid
                 /get?type=raw
        :return:
        '''
        # 是否需要未处理的数据
        proxy_type = request.args.get('type')
        type = proxy_type if proxy_type else 'valid'
        response = WebResponse()
        store_type = current_app.config.get('DATA_STORE_TYPE')
        if store_type == 'mysql':
            db = sql
            if type == 'valid':
                # .order_by(
                # desc(ProxyValid.total))
                data = db.session.query(ProxyValid).filter(ProxyValid.quality == 100).order_by(
                    desc(ProxyValid.total)).all()
            else:
                data = db.session.query(ProxyRaw).order_by(desc(ProxyRaw.gmt_modified)).all()
        else:
            if type == 'valid':
                db = RedisHelper(jobs.PROXY_VALID_KEY)
            else:
                db = RedisHelper(jobs.PROXY_RAW_KEY)
            data = db.getAll()
        if data:
            random_choice = random.choice(data)
            if store_type == 'mysql':
                response.data = random_choice.serialize()
            else:
                response.data = json.loads(random_choice)
        else:
            response.code = WebResponseCode.NO_RECORD
        return response.tojson()


@nsproxy.route("/get_new")
class ProxyGetNewController(BaseResource):
    '''
    获取最新的记录，可能不稳定
    '''
    def get(self):
        response = WebResponse()
        store_type = current_app.config.get('DATA_STORE_TYPE')
        if store_type == 'mysql':
            db = sql
            data = db.session.query(ProxyValid).all()
        else:
            db = RedisHelper(jobs.PROXY_VALID_KEY)
            data = db.getAll()
        if data:
            items = [item for item in data if
                     item.serialize().get('total') == 1 and item.serialize().get('success') == 1]
            random_choice = random.choice(items)
            if store_type == 'mysql':
                item = random_choice.serialize()
            else:
                item = json.loads(random_choice)
            response.data = item
        else:
            response.code = WebResponseCode.NO_RECORD
        return response.tojson()


@nsproxy.route("/get_valid")
class ProxyGetAllValidController(BaseResource):
    def get(self):
        response = WebResponse()
        store_type = current_app.config.get('DATA_STORE_TYPE')
        if store_type == 'mysql':
            db = sql
            data = db.session.query(ProxyValid).all()
        else:
            db = RedisHelper(jobs.PROXY_VALID_KEY)
            data = db.getAll()
        if data:
            if store_type != 'mysql':
                data = [Proxy.fromJson(item) for item in data]
            else:
                data = [item.serialize() for item in data]
            response.data = data
        else:
            response.code = WebResponseCode.NO_RECORD
        return response.tojson()


@nsproxy.route("/get_raw")
class ProxyGetAllRawController(BaseResource):
    def get(self):
        response = WebResponse()
        store_type = current_app.config.get('DATA_STORE_TYPE')
        if store_type == 'mysql':
            db = sql
            data = db.session.query(ProxyRaw).all()
        else:
            db = RedisHelper(jobs.PROXY_RAW_KEY)
            data = db.getAll()
        if data:
            if store_type != 'mysql':
                data = [Proxy.fromJson(item) for item in data]
            else:
                data = [item.serialize() for item in data]
            response.data = data
        else:
            response.code = WebResponseCode.NO_RECORD
        return response.tojson()


@nsproxy.route("/number")
class ProxyGetNumberController(BaseResource):
    def get(self):
        response = WebResponse()
        store_type = current_app.config.get('DATA_STORE_TYPE')
        if store_type == 'mysql':
            db = sql
            valid_number = db.session.query(ProxyValid).count()
            raw_number = db.session.query(ProxyRaw).count()
        else:
            db = RedisHelper(jobs.PROXY_VALID_KEY)
            valid_number = db.len()
            db.change(jobs.PROXY_RAW_KEY)
            raw_number = db.len()
        data = {'raw': raw_number, 'valid': valid_number}
        response.data = data
        return response.tojson()
