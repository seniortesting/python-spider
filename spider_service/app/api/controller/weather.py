# -*- coding:utf-8 -*-
import logging

from flask import request
from flask_restx import Namespace

from app.spider.toutiao.toutiao_weather import ToutiaoWeather
from app.api.util.base_resource import BaseResource
from app.api.util.web_response import WebResponse
from app.api.util.web_responsecode import WebResponseCode

log = logging.getLogger(__name__)
nsweather = Namespace('weather', description='天气接口')


@nsweather.route("")
class WeatherController(BaseResource):
    def get(self):
        '''
        city: 城市名称
        :return:
        '''
        response = WebResponse()
        city = request.values.get('city')
        if city:
            weather = ToutiaoWeather().weather(city)
        else:
            response.code = WebResponseCode.INVALID_PARAMETER
            response.msg = '城市名称不能为空'
            return response.tojson()
        if weather:
            response.data = weather
        else:
            response.code = WebResponseCode.FAILED
        return response.tojson()
