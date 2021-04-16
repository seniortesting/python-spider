# -*- coding:utf-8 -*-
import datetime
import logging

from flask import current_app

from app import jobs
from app.managers.proxy_fetch import FetchFreeProxy
from app.models.models import ProxyRaw
from app.models.proxy import Proxy
from app.utils.db.redis_helper import RedisHelper
from app.utils.spider_utils import verifyProxyFormat
from app.extension import db as sql, schedule

log = logging.getLogger(__name__)


def FetchJob():
    # 通过scheduler得到对应的app context对象
    app= schedule.app
    with app.app_context():
         store_type = current_app.config.get('DATA_STORE_TYPE')
    if store_type == 'mysql':
        db = sql
    else:
        db = RedisHelper(jobs.PROXY_RAW_KEY)
    import inspect
    member_list = inspect.getmembers(FetchFreeProxy, predicate=inspect.isfunction)
    proxy_set = set()
    for func_name, func in member_list:
        log.debug(u"开始获取代理: {}".format(func_name))
        try:
            for proxy in func():
                proxy = proxy.strip()
                if not proxy or not verifyProxyFormat(proxy):
                    log.error('ProxyFetch - {func}: '
                              '{proxy} illegal'.format(func=func_name, proxy=proxy.ljust(20)))
                    continue
                elif proxy in proxy_set:
                    log.debug('ProxyFetch - {func}: '
                             '{proxy} exist'.format(func=func_name, proxy=proxy.ljust(20)))
                    continue
                else:
                    log.debug('ProxyFetch - {func}: '
                             '{proxy} success'.format(func=func_name, proxy=proxy.ljust(20)))
                    # 保存数据
                    last_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                    p = Proxy(name=func_name, proxy=proxy, last_time=last_time)
                    # 持久化保存
                    if store_type == 'mysql':
                        record = ProxyRaw(name=func_name,proxy=proxy,https=False,gmt_create=last_time,gmt_modified=last_time)
                        with app.app_context():
                            db.session.add(record)
                            db.session.commit()
                    else:
                        db.add(p.proxy, p.Json)
                    # 保存到set中检查是否重复
                    proxy_set.add(p)
        except Exception as e:
            log.error(u"代理获取函数 {} 运行出错!".format(func_name))
    # 执行相关统计数据
    log.debug('本次插入代理总数: %s', len(proxy_set))
