# -*- coding:utf-8 -*-
# from redis import Redis, BlockingConnectionPool

from app.extension import redis


class RedisHelper(object):

    def __init__(self, name):
        self.name = name

    def change(self, name):
        self.name = name

    def get(self, key):
        data = redis.hget(name=self.name, key=key)
        return data.decode('utf-8') if data else None

    def getAll(self):
        item_dict = redis.hgetall(self.name)
        return [value.decode('utf8') for key, value in item_dict.items()]

    def add(self, key, value):
        data = redis.hset(self.name, key=key, value=value)
        return data

    def delete(self, key):
        redis.hdel(self.name, key)

    def clear(self):
        return redis.delete(self.name)

    def exists(self, key):
        redis.exists(self.name, key)

    def len(self):
        return redis.hlen(self.name)
