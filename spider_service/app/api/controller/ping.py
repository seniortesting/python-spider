# -*- coding:utf-8 -*-
import logging
from datetime import datetime

from flask_restx import Namespace

from app.api.util.base_resource import BaseResource
from app.api.util.web_response import WebResponse
from app.api.util.web_responsecode import WebResponseCode

log = logging.getLogger(__name__)
nsping = Namespace('ping', description='测试模块接口')


@nsping.route("/hello")
class Ping(BaseResource):
    def get(self):
        response = WebResponse.getResponse()
        result = self.execute('update sys_city set update_time=:t', {'t': datetime.now()})
        log.info(result)
        response.code = WebResponseCode.SUCCESS
        response.data = '测试接口'
        return response.tojson()
