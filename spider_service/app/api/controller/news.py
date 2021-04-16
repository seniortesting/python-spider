# -*- coding:utf-8 -*-
import logging

from flask import request
from flask_restx import Namespace

from app.spider.csdn.csdn import CSDN
from app.spider.toutiao.toutiao_hotnews import ToutiaoNews
from app.api.util.base_resource import BaseResource
from app.api.util.web_response import WebResponse
from app.api.util.web_responsecode import WebResponseCode

log = logging.getLogger(__name__)
nsnews = Namespace('news', description='新闻资讯接口')


@nsnews.route("/toutiao")
class NewsController(BaseResource):
    def get(self):
        '''
        获取头条热点新闻
        refresh: 1,0,true,false
        last: 最后一次的刷新索引值
        :return:
        '''
        response = WebResponse()
        refresh = request.values.get('refresh') in [1, '1', 'true', 'True', True]
        last = request.values.get('last') if request.values.get('last') is not None else 0
        news = ToutiaoNews().hotnews(refresh, last_max_behot_time=last)
        if news:
            response.data = {
                'result': news.get('data'),
                'has_more': news.get('has_more'),
                'next': news.get('next')
            }
        else:
            response.code = WebResponseCode.FAILED
        return response.tojson()


@nsnews.route("/csdn")
class CSDNController(BaseResource):
    def get(self):
        '''
        获取csdn热点科技资讯
        :return:
        '''
        response = WebResponse()
        last = request.values.get('last') if request.values.get('last') is not None else ''
        news = CSDN().getHotNews(last)
        if news:
            response.data = news
        else:
            response.code = WebResponseCode.FAILED
        return response.tojson()
