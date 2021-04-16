# -*- coding:utf-8 -*-
import datetime
import decimal
import json

from app.utils.spider_utils import validProxy


class Proxy(object):

    def __init__(self,
                 name,
                 proxy,
                 https="",
                 proxy_type="",
                 china="",
                 location="",
                 success=0,
                 fail=0,
                 total=0,
                 quality=0,
                 last_status="",
                 last_time=""):
        self._name = name
        self._proxy = proxy
        self._https = https
        self._type = proxy_type
        self._china = china
        self._location = location
        self._success = success
        self._fail = fail
        self._total = total
        self._quality = quality
        self._last_status = last_status
        self._last_time = last_time

    @property
    def name(self):
        return self._name

    @property
    def proxy(self):
        """ 代理 ip:port """
        return self._proxy

    @proxy.setter
    def proxy(self, value):
        self._proxy = value

    @property
    def https(self):
        """ 代理 http/https"""
        return self._https

    @https.setter
    def https(self, value):
        self._https = value

    @property
    def type(self):
        """ 代理 type """
        return self._type

    @type.setter
    def type(self, value):
        self._type = value

    @property
    def china(self):
        """ 代理 china """
        return self._china

    @china.setter
    def china(self, vaue):
        self._china = vaue

    @property
    def location(self):
        """ 代理 ip:port """
        return self._location

    @location.setter
    def location(self, value):
        self._location = value

    @property
    def success(self):
        """ 代理 ip:port """
        return self._success

    @success.setter
    def success(self, value):
        self._success = value

    @property
    def fail(self):
        """ 代理 ip:port """
        return self._fail

    @fail.setter
    def fail(self, value):
        self._fail = value

    @property
    def total(self):
        """ 代理 ip:port """
        return self._total

    @total.setter
    def total(self, value):
        self._total = value

    @property
    def quality(self):
        """ 代理 ip:port """
        return self._quality

    @quality.setter
    def quality(self, value):
        self._quality = value

    @property
    def last_status(self):
        """ 代理 ip:port """
        return self._last_status

    @last_status.setter
    def last_status(self, value):
        self._last_status = value

    @property
    def last_time(self):
        """ 代理 ip:port """
        return self._last_time

    @last_time.setter
    def last_time(self, value):
        self._last_time = value

    @classmethod
    def fromJson(cls, proxy_json):
        """
        根据proxy属性json创建Proxy实例
        :param proxy_json:
        :return:
        """
        proxy_dict = json.loads(proxy_json)
        return cls(name=proxy_dict.get('name', ''),
                   proxy=proxy_dict.get("proxy", ""),
                   https=proxy_dict.get("https", 0),
                   proxy_type=proxy_dict.get("proxy_type", ""),
                   china=proxy_dict.get("china", 0),
                   location=proxy_dict.get("location", ""),
                   success=proxy_dict.get("success", 0),
                   fail=proxy_dict.get("fail", 0),
                   total=proxy_dict.get("total", 0),
                   quality=proxy_dict.get("quality", 0),
                   last_status=proxy_dict.get("last_status", ""),
                   last_time=proxy_dict.get("last_time", "")
                   )

    @property
    def Json(self):
        """ 属性json格式 """
        json_data = json.dumps(self.dict, ensure_ascii=False)
        return json_data

    @property
    def dict(self):
        """ 属性字典 """
        dic = {
            "name": self._name,
            "proxy": self._proxy,
            "https": self._https,
            "proxy_type": self._type,
            "china": self._china,
            "location": self._location,
            "success": self._success,
            "fail": self._fail,
            "total": self._total,
            "quality": self._quality,
            "last_status": self._last_status,
            "last_time": self._last_time}

        return dic

    def validateProxy(self):
        self._total += 1
        if validProxy(self._proxy):
            # 检测通过 更新proxy属性
            self._success += 1
            self._quality = str(decimal.Decimal(self._success / self._total).quantize(decimal.Decimal('.01'),
                                                                                  rounding=decimal.ROUND_DOWN)*100)
            self._last_status = 1
            self._last_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            if self._fail > 0:
                self._fail -= 1
            return self, True
        else:
            self._fail += 1
            if self._success > 0:
                self._success -= 1
            self._quality = str(decimal.Decimal(self._success / self._total).quantize(decimal.Decimal('.01'),
                                                                                  rounding=decimal.ROUND_DOWN)*100)
            self._last_status = 0
            self._last_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

            return self, False
