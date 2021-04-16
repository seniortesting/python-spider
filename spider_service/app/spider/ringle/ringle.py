import logging

from lxml import etree

from app.api.util.web_request import WebRequest

logging.basicConfig(level=logging.INFO,
                    format='[%(asctime)s.%(msecs).03d - %(filename)s:%(lineno)d %(levelname)s]: %(message)s')
log = logging.getLogger(__name__)

inviteUrl = 'https://www.kouling.cn/invite/index/'


class Ringle(object):
    def __init__(self):
        self.http = WebRequest()

    def getRingleCode(self):
        params = {
            'icode': 'K1WoyUJH',
            'k': '小程序开发',
            'id': 'FK1id0e9s5HbeQhaSuwN8g%3D%3D'
        }
        try:
            content = self.http.pc().get(inviteUrl, params=params).text
            html = etree.HTML(content)
            code = html.xpath('//*[@id="code"]/text()')[0]
        except Exception as e:
            log.error('获取邀请码报错: {}', e)
            code = None
        return code


if __name__ == '__main__':
    r = Ringle()
    r.getRingleCode()
