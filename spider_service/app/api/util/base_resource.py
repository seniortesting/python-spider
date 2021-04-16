# -*- coding:utf-8 -*-
import logging

import pymysql
from flask import request
from flask_restx import Resource
from flask_sqlalchemy import Model
from sqlalchemy import text
from sqlalchemy.orm import Session

from app.api.model.models import Base
from app.extension import db

log = logging.getLogger(__name__)


# 关于区别： https://stackoverflow.com/questions/34322471/sqlalchemy-engine-connection-and-session-difference
class BaseResource(Resource):
    @property
    def session(self) -> Session:
        '''
        session for orm operation
        connection for sql operation
        :return:
        '''
        return db.session

    def execute(self, sql: str, params: dict = {}, bind=None) -> list:
        '''
        执行sql查询操作，单表的update,delete,insert请使用orm
        例如:
         execute('SELECT * FROM user WHERE id=:id', {'id': 100})
        :param sql:
        :param params:
        :param bind:
        :return: lastrowid, 插入id
                 returns_rows，返回组
                 rowcount： 数据条数
        '''
        engine = db.get_engine(bind=bind)
        log.info('正在执行SQL: %s, 传递的参数是: %s,......', sql, params)
        try:
            with engine.connect() as connection:
                result = connection.execute(text(sql).execution_options(autocommit=True), params)
                # 查询语句
                if result.returns_rows:
                    dicResult = [dict(row) for row in result]
                    return dicResult
                # 插入语句
                elif result.lastrowid is not None and result.lastrowid != 0:
                    return result.lastrowid
                else:
                    return result.rowcount

        except Exception as e:
            log.error('执行sql:%s, 传递的参数是: %s, 遇到未捕获的异常: %s', sql,
                      str(params), e)
            return None

    @DeprecationWarning
    def save(self, model: Base):
        self.session.add(model)
        self.session.commit()
        return model  # 包含对应的生成的id

    def call(self, spname: str, params: tuple = None, bind=None) -> tuple:
        '''
        call the store procedure using sql
        :rtype: object
        :param spname:
        :param params:
        :return: tuple
        '''
        connection = db.get_engine(bind=bind).raw_connection()
        log.info('正在执行存储过程: %s, 传递的参数是: %s,......', spname, params)
        resultsetList = []
        paramsResultList = []
        try:
            with connection.cursor(cursor=pymysql.cursors.DictCursor) as cursor:
                params = params if params is not None else ()
                paramsCallbackResult = cursor.callproc(spname, args=params)
                log.debug('返回的输出值是: %s' % str(paramsCallbackResult))
                resultsetList = cursor.fetchall()
                if isinstance(resultsetList, tuple):
                    resultsetList = list(resultsetList)
                # cursor.close()
                connection.commit()
                if params:
                    sql = 'SELECT '
                    for index in range(len(paramsCallbackResult)):
                        sql += '@_%s_%s, ' % (spname, index)
                    sql = sql.strip()[:-1]
                    cursor.execute(sql)
                    paramsResultList = cursor.fetchall()
                    # paramsResultList = list(paramsCallbackResult)
                    log.debug('带参数的存储过程返回结果是: %s' % (str(paramsResultList)))
                else:
                    paramsResultList = paramsCallbackResult
                    log.debug('不带参数的存储过程返回结果是: %s' % (str(paramsCallbackResult)))
        except Exception as e:
            log.error('调用存储过程:%s, 传递的参数是: %s, 遇到未捕获的异常: %s', spname,
                      params, e)
        finally:
            connection.close()
        return paramsResultList, resultsetList

    def callFirstOutputValue(self, outputParameters) -> str:
        if isinstance(outputParameters, list):
            if len(outputParameters) > 0:
                paramsdict = outputParameters[0]
                # orderedParamList = list(collections.OrderedDict(paramsdict).items())
                # paramsTuple = orderedParamList[-1]
                # 如果参数超过10个此时的sorted,排列的key是不对的,
                # 此处的items类似如下的结构:
                # dict_items([('@_project_AddEngineeringQuantity_2', 13), ('@_project_AddEngineeringQuantity_0', 18), ('@_project_AddEngineeringQuantity_3', 1), ('@_project_AddEngineeringQuantity_1', '333'), ('@_project_AddEngineeringQuantity_12', '333')])
                # 把key进行截取得到最后的的一段字符串序号进行排序
                sortedListTuple = sorted(paramsdict.items(), key=lambda item: int(item[0].split('_')[-1]))
                # paramsTuple = list(collections.OrderedDict(sorted(paramsdict.items())).items())[-1]
                # sortedDict=collections.OrderedDict(paramsdict.items())
                lastTupleElement = sortedListTuple[-1]
                # lastElementKey=next(reversed(sortedDict))
                # lastElement=sortedDict.get(lastElementKey)
                return lastTupleElement[-1]  # 得到最后的一个outputparameter对应的output的value
            else:
                return 0
        else:
            return outputParameters[-1]

    def json(self):
        return request.json
