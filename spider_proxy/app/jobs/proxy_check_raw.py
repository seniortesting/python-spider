# -*- coding:utf-8 -*-
import logging
import time
from multiprocessing import Queue, Process

from flask import current_app

from app import jobs
from app.models.models import ProxyRaw, ProxyValid
from app.models.proxy import Proxy
from app.utils.db.redis_helper import RedisHelper
from app.utils.spider_utils import getCpuNumber
from app.extension import db as sql, schedule

log = logging.getLogger(__name__)


def checkRawProxyJob():
    app = schedule.app
    with app.app_context():
        store_type = current_app.config.get('DATA_STORE_TYPE')
    if store_type == 'mysql':
        db = sql
    else:
        db = RedisHelper(jobs.PROXY_RAW_KEY)
    proxy_queue = Queue()
    # 此处直接装填队列，因为进程已经启动好了，此时只要一个队列有数据，就有一个进程进行处理
    if store_type == 'mysql':
        with app.app_context():
            data = db.session.query(ProxyRaw).all()
            data = [Proxy(name=item.name, proxy=item.proxy, https=item.https,
                          success=item.success if item.success else 0, fail=item.fail if item.fail else 0,
                          total=item.total if item.total else 0, quality=item.quality if item.quality else 0,
                          last_time=item.gmt_modified) for item in data]
    else:
        data = db.getAll()
    if len(data) > 0:
        for proxy in data:
            proxy_queue.put(proxy)
            # 很奇怪的问题,会导致Queue退出,BrokenPipeError: [Errno 32] Broken pipe
            time.sleep(0.01)
        # 清除临时旧数据库
        if store_type == 'mysql':
            with app.app_context():
                db.session.query(ProxyRaw).delete()
        else:
            db.clear()
        # 启动多进行进行检查所有的代理地址是否合法
        process_list = list()
        num = getCpuNumber()
        for index in range(num):
            process = Process(target=CheckProcess(proxy_queue).run())
            process.daemon = True
            process_list.append(process)
        for work in process_list:
            work.start()
        # 终止所有的进程操作
        for _ in process_list:
            proxy_queue.put(None)

        for work in process_list:
            work.join()
        log.debug("RawProxyCheck - 本次验证执行结束,验证数量: {}".format(len(data)))


class CheckProcess(object):

    def __init__(self, queue: Queue):
        self.queue = queue
        app = schedule.app
        with app.app_context():
            self.store_type = current_app.config.get('DATA_STORE_TYPE')
        if self.store_type == 'mysql':
            self.db = sql
        else:
            self.db = RedisHelper(jobs.PROXY_VALID_KEY)

    def run(self):
        if self.store_type != 'mysql':
            self.db.change(jobs.PROXY_VALID_KEY)
        while True:
            if self.queue.empty(): break
            proxy_data = self.queue.get()
            if proxy_data is None: break
            if self.store_type != 'mysql':
                proxyObj = Proxy.fromJson(proxy_data)
            else:
                proxyObj = proxy_data
            proxy, status = proxyObj.validateProxy()
            if status:
                # 保存到数据库中
                if self.store_type != 'mysql':
                    self.db.add(proxy.proxy, proxy.Json)
                else:
                    proxy_valid = ProxyValid(name=proxy.name, proxy=proxy.proxy, https=proxy.https,
                                             proxy_type=proxy.type, china=proxy.china, location=proxy.location,
                                             success=proxy.success, fail=proxy.fail, total=proxy.total,
                                             quality=proxy.quality,
                                             last_status=proxy.last_status, gmt_modified=proxy.last_time)
                    app = schedule.app
                    with app.app_context():
                        self.db.session.add(proxy_valid)
                        self.db.session.commit()
                log.debug('RawProxyCheck - {}  : {} validation pass'.format(proxy.name, proxy.proxy.ljust(20)))
            else:
                log.error(
                    'RawProxyCheck - {}  : {}, into time: {} validation fail'.format(proxy.name, proxy.proxy.ljust(20),
                                                                                     proxy.last_time))
