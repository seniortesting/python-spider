from unittest import TestCase


# -*- coding:utf-8 -*-
from bs4 import BeautifulSoup

from app.api.util.web_request import WebRequest

class TestHttp(TestCase):
    def test_get(self):
        http=WebRequest()
        content=http.get('https://www.ipip.net/').text
        bs=BeautifulSoup(content,'lxml')
        ip=bs.select_one('div.outer.indexBanner > div > ul > li:nth-child(1) > a').text
        print(ip)
