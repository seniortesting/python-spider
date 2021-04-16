import decimal
from unittest import TestCase


# -*- coding:utf-8 -*-
class TestRedisHelper(TestCase):
    def test_get(self):
        a=decimal.Decimal(4/6).quantize(decimal.Decimal('.01'), rounding=decimal.ROUND_DOWN)
        print(a)

    def test_getAll(self):
        self.fail()

    def test_add(self):
        self.fail()

    def test_delete(self):
        self.fail()

    def test_clear(self):
        self.fail()

    def test_exists(self):
        self.fail()

    def test_len(self):
        self.fail()
