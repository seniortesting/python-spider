# -*- coding:utf-8 -*-
from enum import Enum


class WebResponseCode(Enum):
    SUCCESS = (1000, '成功')
    FAILED = (5000, "失败")
    NOT_FOUND = (1004, '没有找到页面资源')
    INVALID_PARAMETER = (1001, '输入参数错误')
    INTERNAL_SERVER_ERROR = (1002, '服务器未捕获的异常')

    NO_RECORD = (1003, '没有这个记录')
    DUPLICATED_RECORD = (1005, '数据重复')
    NO_CHANGE = (1006, '数据没有改变')

    def __init__(self, code, description):
        self.__code = code
        self.__decription = description

    @property
    def code(self) -> int:
        return self.__code

    @property
    def msg(self) -> str:
        return self.__decription
