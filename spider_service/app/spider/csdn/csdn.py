# -*- coding:utf-8 -*-

from app.api.util.web_request import WebRequest

http = WebRequest()


class CSDN(object):

    def getHotNews(self, offset=None):
        '''
        爬取热点新闻
        :param offset:
        :return:
        '''
        json_data = None
        url = 'https://www.csdn.net/api/articles'
        params = {
            'type': 'more',
            'category': 'python',
            'shown_offset': offset if offset else ''
        }
        resp = http.pc().get(url, params=params)
        valid = resp.status_code == 200
        if valid:
            json_data = resp.json()
        return json_data


if __name__ == '__main__':
    csdn = CSDN()
    csdn.getHotNews()
