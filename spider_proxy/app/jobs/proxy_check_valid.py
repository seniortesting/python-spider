# -*- coding:utf-8 -*-
import logging
import time
from multiprocessing import Queue, Process

from flask import current_app

from app import jobs
from app.models.models import ProxyValid
from app.models.proxy import Proxy
from app.utils.db.redis_helper import RedisHelper
from app.utils.spider_utils import getCpuNumber
from app.extension import db as sql, schedule

log = logging.getLogger(__name__)

FAIL_COUNT = 0


def checkValidProxyJob():
    app = schedule.app
    with app.app_context():
       store_type = current_app.config.get('DATA_STORE_TYPE')
    if store_type == 'mysql':
        db = sql
    else:
        db = RedisHelper(jobs.PROXY_VALID_KEY)
    proxy_queue = Queue()
    # 此处直接装填队列，因为进程已经启动好了，此时只要一个队列有数据，就有一个进程进行处理
    if store_type == 'mysql':
        with app.app_context():
            data =db.session.query(ProxyValid).all()
            data =[ Proxy(name=item.name,proxy=item.proxy,https=item.https,
                          success=item.success if item.success else 0,fail=item.fail if item.fail else 0,
                          total=item.total if item.total else 0,quality=item.quality if item.quality else 0,
                          last_time=item.gmt_modified)  for item in data]
    else:
        data = db.getAll()
    if len(data) > 0:
        for proxy in data:
            proxy_queue.put(proxy)
            # 很奇怪的问题,会导致Queue退出,BrokenPipeError: [Errno 32] Broken pipe
            time.sleep(0.01)
        # 启动多进行进行检查所有的代理地址是否合法
        process_list = list()
        num = getCpuNumber()
        for index in range(num):
            process = Process(target=CheckProcess(proxy_queue).run())
            process.daemon = True
            process_list.append(process)
            log.info("添加代理检查进程: {}".format(str(process)))
        for work in process_list:
            work.start()
        # 终止所有的进程操作
        for _ in process_list:
            proxy_queue.put(None)

        for work in process_list:
            work.join()
        log.debug("ValidProxyCheck - 本次验证执行结束,验证数量: {}".format(len(data)))
    else:
        log.warning("ValidProxyCheck - 本次查询数据为空,不进行数据校验!")


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
            # log.info('正在运行代理检查,检查队列是: {}'.format(self.queue.qsize()))
            proxy_data = self.queue.get()
            if proxy_data is None: break
            if self.store_type != 'mysql':
                proxyObj = Proxy.fromJson(proxy_data)
            else:
                proxyObj = proxy_data
            proxy, status = proxyObj.validateProxy()
            # log.info('执行检查结果: {}, 结果是: {}'.format(str(proxy),status))
            if status or proxy.fail < FAIL_COUNT:
                # 保存到数据库中
                if self.store_type != 'mysql':
                    if self.db.exists(proxy.proxy):
                        log.debug('ValidProxyCheck - {}  : {} validation exists'.format(proxy.name,
                                                                                       proxy.proxy.ljust(20)))
                    self.db.add(proxy.proxy, proxy.Json)
                else:
                    app = schedule.app
                    with app.app_context():
                        proxy_info=self.db.session.query(ProxyValid).filter(ProxyValid.proxy==proxy.proxy).first()
                        proxy_info.success=proxy.success
                        proxy_info.fail=proxy.fail
                        proxy_info.total=proxy.total
                        proxy_info.quality=proxy.quality
                        proxy_info.last_status=proxy.last_status
                        proxy_info.gmt_modified= proxy.last_time
                        self.db.session.commit()
                log.debug('ValidProxyCheck - {}  : {} validation pass'.format(proxy.name, proxy.proxy.ljust(20)))
            else:
                log.debug('ValidProxyCheck - {}  : {} validation fail'.format(proxy.name, proxy.proxy.ljust(20)))
                if self.store_type != 'mysql':
                   self.db.delete(proxy.proxy)
                else:
                    app = schedule.app
                    with app.app_context():
                        self.db.session.query(ProxyValid).filter(ProxyValid.proxy==proxy.proxy).delete()
