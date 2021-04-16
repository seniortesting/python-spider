# -*- coding:utf-8 -*-

class Test_URL_Fail(Exception):

    def __init__(self, msg):
        self.msg = msg

    def __str__(self):
        str = "访问%s失败，请检查网络连接" % self.msg
        return str


class Con_DB_Fail(Exception):
    def __init__(self, msg):
        self.msg = msg

    def __str__(self):
        str = "使用DB_CONNECT_STRING:%s--连接数据库失败" % self.msg
        return str
