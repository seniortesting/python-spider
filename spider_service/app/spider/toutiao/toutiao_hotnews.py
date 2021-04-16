# -*- coding:utf-8 -*-
import logging
import os

import js2py

from app.api.util.web_request import WebRequest

logging.basicConfig(level=logging.INFO,
                    format='[%(asctime)s.%(msecs).03d - %(filename)s:%(lineno)d %(levelname)s]: %(message)s')
log = logging.getLogger(__name__)

'''
该脚本为爬取今日头条的每日热点内容
分析步骤：
1. 发现as,cp和signature是动态的参数,还有一个cookie参数需要设置：
2. 分析js脚本：<script src="//s3a.pstatp.com/toutiao/resource/ntoutiao_web/page/home/whome/home_97feb13.js"></script>

'''
HOT_PC_URL = 'https://www.toutiao.com/api/pc/feed/'
HOT_MOBILE_URL = 'https://m.toutiao.com/list/'


class ToutiaoNews(object):

    def __init__(self):
        self.http = WebRequest()
        self.context = js2py.EvalJs()

    def getascp(self):
        path = os.path.join(os.path.dirname(__file__), 'get_as_cp.js')
        with open(path, 'r', encoding='UTF-8') as f:
            js = f.read()
        self.context.eval(js)
        result = self.context.getHoney()
        resultDict = result.to_dict()
        as_ = resultDict['as']
        cp = resultDict['cp']
        return as_, cp

    def get_signature(self, item_id):
        # with SpiderWebDriver('https://www.toutiao.com/ch/news_hot/') as spider:
        #     # spider.execute_script(f'return TAC.sign({max_behot_time_tmp})')
        #     signature = spider.execute_script(f'return TAC.sign(0)')
        #     print(f'列表页signature参数：{signature}')
        path = os.path.join(os.path.dirname(__file__), 'get_signature.js')
        with open(path, 'r', encoding='UTF-8') as f:
            js = f.read()
        self.context.eval(js)
        signature = self.context.get_signature(item_id)
        print(signature)
        return signature

    def hotnews(self, refresh=True, last_max_behot_time=0):
        try:
            as_, cp = self.getascp()
            # 如果是0代表的是refresh，否则参数是 max_behot_time_tmp
            if refresh:
                max_behot_time = 0
                max_behot_time_tmp = last_max_behot_time
                # signature = get_signature(0)
            else:
                max_behot_time = last_max_behot_time
                max_behot_time_tmp = last_max_behot_time
                # signature = get_signature(last_max_behot_time)

            # 请求参数
            pc_params = {
                'category': 'news_hot',
                'utm_source': 'toutiao',
                'widen': 1,
                'max_behot_time': max_behot_time,
                'max_behot_time_tmp': max_behot_time_tmp,
                'tadrequire': 'true',
                'as': as_,
                'cp': cp
            }
            # mobile_params = {
            #     'tag': 'news_hot',
            #     'ac': 'wap',
            #     'count': '20',
            #     'format': 'json_raw',
            #     'as': 'A1F56DF4AB1927C',
            #     'cp': '5D4B09C2B7ACEE1',
            #     'min_behot_time': '1565233760',
            #     '_signature': 'V0ZowgAACg5eChLXjmCm4ldGaN',
            #     'i': '1565225343'
            # }
            headers = {
                'accept': 'text/javascript, text/html, application/xml, text/xml, */*',
                'content-type': 'application/x-www-form-urlencoded',
                'referer': 'https://www.toutiao.com/ch/news_hot/'
            }
            cookies = {
                'tt_webid': '6700427857275422221'
            }
            response = self.http.pc().get(url=HOT_PC_URL, params=pc_params, headers=headers, cookies=cookies)
            result = response.json()
        except Exception as e:
            log.error('调用新闻接口失败，异常信息如下:', exc_info=True)
            result = None

        return result

    def save_db(self):
        pass


def main():
    max_behot_time = 0
    for page in range(1, 3):
        result = ToutiaoNews().hotnews(True, max_behot_time)
        log.info(result)
        max_behot_time = result['next']['max_behot_time']


if __name__ == '__main__':
    main()
