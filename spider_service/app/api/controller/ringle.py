# -*- coding:utf-8 -*-

import logging

from flask_restx import Namespace

from app.spider.ringle.ringle import Ringle
from app.api.util.base_resource import BaseResource
from app.api.util.web_response import WebResponse
from app.api.util.web_responsecode import WebResponseCode

log = logging.getLogger(__name__)
nsringle = Namespace('ringle', description='灵鸽接口')


@nsringle.route("")
class RingleController(BaseResource):
    def get(self):
        '''
        获取灵鸽对应的邀请码
        :return:
        '''
        response = WebResponse()
        r = Ringle()
        code = r.getRingleCode()
        if code is not None:
            response.data = code
        else:
            response.code = WebResponseCode.FAILED
        return response.tojson()
