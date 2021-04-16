# -*- coding:utf-8 -*-
import multiprocessing

import requests
from lxml import etree

from app.utils.web_request import WebRequest

def getCpuNumber():
    if multiprocessing.cpu_count() < 3:
        number = multiprocessing.cpu_count()
    else:
        number = multiprocessing.cpu_count() - 1
    return number

def verifyProxyFormat(proxy):
    """
    检查代理格式
    :param proxy:
    :return:
    """
    import re
    verify_regex = r"\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}:\d{1,5}"
    _proxy = re.findall(verify_regex, proxy)
    return True if len(_proxy) == 1 and _proxy[0] == proxy else False


def getHtmlTree(url, **kwargs):
    """
    获取html树
    :param url:
    :param kwargs:
    :return:
    """

    header = {'Connection': 'keep-alive',
              'Cache-Control': 'max-age=0',
              'Upgrade-Insecure-Requests': '1',
              'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_3) AppleWebKit/537.36 (KHTML, like Gecko)',
              'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
              'Accept-Encoding': 'gzip, deflate, sdch',
              'Accept-Language': 'zh-CN,zh;q=0.8',
              }
    # TODO 取代理服务器用代理服务器访问
    request=WebRequest()
    html = request.get(url=url, headers=header).content
    return etree.HTML(html)


def tcpConnect(proxy):
    """
    TCP 三次握手
    :param proxy:
    :return:
    """
    from socket import socket, AF_INET, SOCK_STREAM
    s = socket(AF_INET, SOCK_STREAM)
    ip, port = proxy.split(':')
    result = s.connect_ex((ip, int(port)))
    return True if result == 0 else False


def validProxy(proxy):
    """
    检验代理是否可用,格式: 192.168.1.1：8080
    :param proxy:
    :return:
    """
    if isinstance(proxy, bytes):
        proxy = proxy.decode('utf8')
    proxies = {"http": "http://{proxy}".format(proxy=proxy), "https": "https://{proxy}".format(proxy=proxy)}
    try:
        # 超过20秒的代理就不要了: http://httpbin.org/ip
        r = requests.get('https://www.baidu.com', proxies=proxies, timeout=3, verify=False)
        if r.status_code == 200:
            # logger.info('%s is ok' % proxy)
            return True
    except Exception as e:
        # logger.error(str(e))
        return False
