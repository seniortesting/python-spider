# -*- coding:utf-8 -*-
import random
import unittest


class MyTestCase(unittest.TestCase):

    def randomGroup(self,list,num):
        random.shuffle(list)
        for i in range(0, len(list), num):
            yield list[i:i + num]

    def test_something(self):
        n = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K']
        r=list(self.randomGroup(n,3))
        print(r)

if __name__ == '__main__':
    unittest.main()
