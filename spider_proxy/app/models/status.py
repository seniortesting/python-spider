# -*- coding:utf-8 -*-
class Status(object):

    def __init__(self,
                 name,
                 success,
                 fail,
                 total,
                 quality):
        self._name = name
        self._success = success
        self._fail = fail
        self._total = total
        self._quality = quality
