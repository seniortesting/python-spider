# -*- coding:utf-8 -*-
import copy
import datetime
import threading
from decimal import Decimal

from flask import jsonify

from app.utils.web_responsecode import WebResponseCode


class WebResponse(object):
    '''
    通用返回结果
    '''

    def __init__(self, code=WebResponseCode.SUCCESS, msg=None, data=None):
        self.code = code
        self.msg = msg
        self.data = data

    # @classmethod
    # def getResponse(cls, *args, **kwargs):
    #     if not hasattr(WebResponse, "_instance"):
    #         with WebResponse._instance_lock:
    #             if not hasattr(WebResponse, "_instance"):
    #                 WebResponse._instance = WebResponse(*args, **kwargs)
    #     return WebResponse._instance

    @staticmethod
    def getResponse():
        return WebResponse()

    #
    # def success(self):
    #     self.code = WebResponseCode.SUCCESS
    #
    # def success(self, data):
    #     self.code = WebResponseCode.SUCCESS
    #     self.data = data
    #
    # def success(self, msg):
    #     self.code = WebResponseCode.SUCCESS
    #     self.msg = msg
    #
    # def success(self, data, msg):
    #     self.code = WebResponseCode.SUCCESS
    #     self.msg = msg
    #     self.data = data
    #
    # def failed(self):
    #     self.code = WebResponseCode.FAILED
    #
    # def failed(self, code):
    #     self.code = code
    #
    # def failed(self, msg):
    #     self.code = WebResponseCode.FAILED
    #     self.msg = msg
    #
    # def failed(self, code, msg):
    #     self.code = code
    #     self.msg = msg

    def tojson(self):
        # return simplejson.dumps(self.__to_dict(), ensure_ascii=False)
        jsondict = self.__to_dict()
        return jsonify(jsondict)
        # return jsondict

    def __to_dict(self):
        nowtime = datetime.datetime.now()
        responsemsg = self.msg if self.msg else self.code.msg
        response_json_dict = dict(code=self.code.code, msg=responsemsg, request_time=nowtime, data=self.data)
        scrubbing = self.__scrubbing(response_json_dict)
        return scrubbing

    def __scrubbing(self, obj):
        """None to empty string"""
        jsondata = copy.deepcopy(obj)
        # Handle dictionaries. Scrub all values
        if isinstance(obj, dict):
            for k, v in jsondata.items():
                jsondata[k] = self.__scrubbing(v)
        elif isinstance(obj, list):
            for i in range(len(jsondata)):
                jsondata[i] = self.__scrubbing(jsondata[i])
        elif isinstance(obj, Decimal):  # Handle Decimal
            jsondata = str(Decimal(obj))
        elif isinstance(obj, (datetime.date)):  # Handle datetime
            # jsondata =obj.isoformat()
            if isinstance(obj, datetime.datetime):
                jsondata = obj.strftime('%Y-%m-%d %H:%M:%S')
            else:
                jsondata = obj.strftime('%Y-%m-%d')
            # jsondata = obj.strftime('%Y{0}%m{1}%d{2} %H:%M:%S').format(*'年月日')
        elif isinstance(obj, datetime.time):  # Handle time
            jsondata = obj.strftime('%H:%M')
        elif isinstance(obj, bytes):  # Handle bytes
            jsondata = ord(obj)
        elif isinstance(obj, WebResponseCode):
            return obj.code
        elif obj is None:  # Handle None
            jsondata = {}
        return jsondata
