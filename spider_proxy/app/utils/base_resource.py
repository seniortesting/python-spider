# -*- coding:utf-8 -*-

# 关于区别： https://stackoverflow.com/questions/34322471/sqlalchemy-engine-connection-and-session-difference
from flask import request
from flask_restplus import Resource

from app.extension import redis


class BaseResource(Resource):
    @property
    def redis(self):
        '''
        session for orm operation
        connection for sql operation
        :return:
        '''
        return redis

    def json(self):
        return request.json
