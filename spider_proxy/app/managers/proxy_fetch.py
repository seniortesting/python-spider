# -*- coding:utf-8 -*-
import logging
import re
from time import sleep

import requests
import urllib3

from app.utils.spider_utils import getHtmlTree, verifyProxyFormat
from app.utils.web_request import WebRequest

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
logging.basicConfig(level=logging.INFO,
                    format='[%(asctime)s.%(msecs).03d - %(filename)s:%(lineno)d %(levelname)s]: %(message)s')
log = logging.getLogger(__name__)


class FetchFreeProxy(object):

    @staticmethod
    def ip66(count=20):
        """
        代理66 http://www.66ip.cn/
        :param count: 提取数量
        :return:
        """
        urls = [
            "http://www.66ip.cn/nmtq.php?getnum=60&isp=0&anonymoustype=0&start=&ports=&export=&ipaddress=&area=1&proxytype=2&api=66ip"
        ]
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:34.0) Gecko/20100101 Firefox/34.0',
                   'Accept': '*/*',
                   'Connection': 'keep-alive',
                   'Accept-Language': 'zh-CN,zh;q=0.8'}
        try:
            import js2py
            session = requests.Session()
            session.verify = False
            # -----------------------------2019-08-16 最早期版本
            # src = session.get("http://www.66ip.cn/", headers=headers).text
            #
            # src = src.split("</script>")[0] + '}'
            # src = src.replace("<script>", "function test() {")
            # src = src.replace("while(z++)try{eval(", ';var num=10;while(z++)try{var tmp=')
            # src = src.replace(");break}", ";num--;if(tmp.search('cookie') != -1 | num<0){return tmp}}")
            # ctx = js2py.eval_js(src)
            # src = ctx.test()
            # src = src[src.find("document.cookie="): src.find("};if((")]
            # src = src.replace("document.cookie=", "")
            # src = "function test() {var window={}; return %s }" % src
            # cookie = js2py.eval_js(src).test()
            # js_cookie = cookie.split(";")[0].split("=")[-1]
            # -----------------------------2019-08-16 更新版本需要破解cookies
            # content = ''.join(re.findall('<script>(.*?)</script>', content))
            # function_js = content.replace('eval', 'return')
            # function_content = "function getClearance(){" + function_js + "};"
            # self.context.execute(function_content)
            # # 一级解密结果
            # decoded_result = self.context.getClearance()
            # function_js_result = 'var a' + decoded_result.split('document.cookie')[1].split("Path=/;'")[
            #     0] + "Path=/;';return a;"
            # # s = re.sub(r'document.create.*?firstChild.href', '"{}"'.format(self.start_url), s)
            # function_content_result = "function getClearanceResult(){" + function_js_result + "};"
            # self.context.execute(function_content_result)
            # # 二次解密结果
            # decoded_content = self.context.getClearanceResult()
            # jsl_clearance = decoded_content.split(';')[0]
        except Exception as e:
            print(e)
            return

        for url in urls:
            try:
                # cookies={"__jsl_clearance": js_cookie}
                html = session.get(url.format(count), headers=headers).text
                ips = re.findall(r"\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}:\d{1,5}", html)
                for ip in ips:
                    yield ip.strip()
            except Exception as e:
                print(e)
                pass

    @staticmethod
    def goubanjia():
        """
        guobanjia http://www.goubanjia.com/
        :return:
        """
        url = "http://www.goubanjia.com/"
        tree = getHtmlTree(url)
        proxy_list = tree.xpath('//td[@class="ip"]')
        # 此网站有隐藏的数字干扰，或抓取到多余的数字或.符号
        # 需要过滤掉<p style="display:none;">的内容
        xpath_str = """.//*[not(contains(@style, 'display: none'))
                                        and not(contains(@style, 'display:none'))
                                        and not(contains(@class, 'port'))
                                        ]/text()
                                """
        for each_proxy in proxy_list:
            try:
                # :符号裸放在td下，其他放在div span p中，先分割找出ip，再找port
                ip_addr = ''.join(each_proxy.xpath(xpath_str))

                # HTML中的port是随机数，真正的端口编码在class后面的字母中。
                # 比如这个：
                # <span class="port CFACE">9054</span>
                # CFACE解码后对应的是3128。
                port = 0
                for _ in each_proxy.xpath(".//span[contains(@class, 'port')]"
                                          "/attribute::class")[0]. \
                        replace("port ", ""):
                    port *= 10
                    port += (ord(_) - ord('A'))
                port /= 8

                yield '{}:{}'.format(ip_addr, int(port))
            except Exception as e:
                pass

    @staticmethod
    def kuaidaili():
        """
        快代理 https://www.kuaidaili.com
        """
        url_list = [
            'https://www.kuaidaili.com/free/inha/',
            'https://www.kuaidaili.com/free/intr/'
        ]
        for url in url_list:
            tree = getHtmlTree(url)
            proxy_list = tree.xpath('.//table//tr')
            sleep(1)  # 必须sleep 不然第二条请求不到数据
            for tr in proxy_list[1:]:
                yield ':'.join(tr.xpath('./td/text()')[0:2])

    @staticmethod
    def coderbusy():
        """
        码农代理 https://proxy.coderbusy.com/
        :return:
        """
        urls = ['https://proxy.coderbusy.com/']
        for url in urls:
            tree = getHtmlTree(url)
            proxy_list = tree.xpath('.//table//tr')
            for tr in proxy_list[1:]:
                tr_data=tr.xpath('./td/text()')
                ip_port=tr_data[0:2]
                location=tr_data[-1].strip()
                if location in ['腾讯云','阿里云','移动','联通','电信', '世纪互联']: yield  ':'.join(ip_port)
                # yield ':'.join(tr.xpath('./td/text()')[0:2])

    @staticmethod
    def ip3366():
        """
        云代理 http://www.ip3366.net/free/
        :return:
        """
        urls = ['http://www.ip3366.net/free/?stype=1',
                "http://www.ip3366.net/free/?stype=2"
                ]
        request = WebRequest()
        for url in urls:
            r = request.get(url, timeout=10)
            proxies = re.findall(r'<td>(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})</td>[\s\S]*?<td>(\d+)</td>', r.text)
            for proxy in proxies:
                yield ":".join(proxy)

    @staticmethod
    def jiangxianli(page_count=2):
        """
        http://ip.jiangxianli.com/?page=
        免费代理库
        :return:
        """
        for i in range(1, page_count + 1):
            url = 'http://ip.jiangxianli.com/?page={}'.format(i)
            html_tree = getHtmlTree(url)
            tr_list = html_tree.xpath("/html/body/div[1]/div/div[1]/div[2]/table/tbody/tr")
            if len(tr_list) == 0:
                continue
            for tr in tr_list:
                yield tr.xpath("./td[2]/text()")[0] + ":" + tr.xpath("./td[3]/text()")[0]

    @staticmethod
    def data5u():
        '''
        无忧代理，免费10个
        :return:
        '''
        url_list = [
            'http://www.data5u.com/',
        ]
        for url in url_list:
            html_tree = getHtmlTree(url)
            ul_list = html_tree.xpath('//ul[@class="l2"]')
            for ul in ul_list:
                try:
                    yield ':'.join(ul.xpath('.//li/text()')[0:2])
                except Exception as e:
                    print(e)

    @staticmethod
    def xicidaili(page_count=1):
        url_list = [
            'http://www.xicidaili.com/nn/',  # 高匿
        ]
        for each_url in url_list:
            for i in range(1, page_count + 1):
                page_url = each_url + str(i)
                tree = getHtmlTree(page_url)
                proxy_list = tree.xpath('.//table[@id="ip_list"]//tr[position()>1]')
                for proxy in proxy_list:
                    try:
                        yield ':'.join(proxy.xpath('./td/text()')[0:2])
                    except Exception as e:
                        pass

    # @staticmethod
    # def proxylistplus():
    #     urls = ['https://list.proxylistplus.com/Fresh-HTTP-Proxy-List-1']
    #     request = WebRequest()
    #     for url in urls:
    #         r = request.get(url)
    #         proxies = re.findall(r'<td>(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})</td>[\s\S]*?<td>(\d+)</td>', r.text)
    #         for proxy in proxies:
    #             yield ':'.join(proxy)

    # @staticmethod
    # def iphai():
    #     """
    #     IP海 http://www.iphai.com/free/ng
    #     :return:
    #     """
    #     urls = [
    #         'http://www.iphai.com/free/ng',
    #         'http://www.iphai.com/free/np',
    #         'http://www.iphai.com/free/wg',
    #         'http://www.iphai.com/free/wp'
    #     ]
    #     request = WebRequest()
    #     for url in urls:
    #         r = request.get(url, timeout=10)
    #         proxies = re.findall(r'<td>\s*?(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})\s*?</td>[\s\S]*?<td>\s*?(\d+)\s*?</td>',
    #                              r.text)
    #         for proxy in proxies:
    #             yield ":".join(proxy)
    # @staticmethod
    # def ip181(days=1):
    #     url = 'http://www.ip181.com/'
    #     html_tree = getHtmlTree(url)
    #     try:
    #         tr_list = html_tree.xpath('//tr')[1:]
    #         for tr in tr_list:
    #             yield ':'.join(tr.xpath('./td/text()')[0:2])
    #     except Exception as e:
    #         pass
    # @staticmethod
    # def mimiip():
    #     url_gngao = ['http://www.mimiip.com/gngao/%s' % n for n in range(1, 10)]  # 国内高匿
    #     url_gnpu = ['http://www.mimiip.com/gnpu/%s' % n for n in range(1, 10)]  # 国内普匿
    #     url_gntou = ['http://www.mimiip.com/gntou/%s' % n for n in range(1, 10)]  # 国内透明
    #     url_list = url_gngao + url_gnpu + url_gntou
    #
    #     request = WebRequest()
    #     for url in url_list:
    #         r = request.get(url)
    #         proxies = re.findall(r'<td>(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})</td>[\w\W].*<td>(\d+)</td>', r.text)
    #         for proxy in proxies:
    #             yield ':'.join(proxy)

    # @staticmethod
    # def xundaili():
    #     '''
    #     讯代理
    #     :return:
    #     '''
    #     url = 'http://www.xdaili.cn/ipagent/freeip/getFreeIps?page=1&rows=10'
    #     request = WebRequest()
    #     try:
    #         res = request.get(url).json()
    #         for row in res['RESULT']['rows']:
    #             yield '{}:{}'.format(row['ip'], row['port'])
    #     except Exception as e:
    #         pass

    # @staticmethod
    # def cnproxy():
    #     urls = ['http://cn-proxy.com/', 'http://cn-proxy.com/archives/218']
    #     request = WebRequest()
    #     for url in urls:
    #         r = request.get(url)
    #         proxies = re.findall(r'<td>(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})</td>[\w\W]<td>(\d+)</td>', r.text)
    #         for proxy in proxies:
    #             yield ':'.join(proxy)
    # @staticmethod
    # def proxylist():
    #     urls = ['https://proxy-list.org/english/index.php?p=%s' % n for n in range(1, 10)]
    #     request = WebRequest()
    #     import base64
    #     for url in urls:
    #         r = request.get(url)
    #         proxies = re.findall(r"Proxy\('(.*?)'\)", r.text)
    #         for proxy in proxies:
    #             yield base64.b64decode(proxy).decode()


def checkAllProxy():
    """
    检查getFreeProxy所有代理获取函数运行情况
    Returns:
        None
    """
    import inspect
    member_list = inspect.getmembers(FetchFreeProxy, predicate=inspect.isfunction)
    proxy_count_dict = dict()
    for func_name, func in member_list:
        log.debug(u"开始运行代理: {}".format(func_name))
        try:
            proxy_list = [_ for _ in func() if verifyProxyFormat(_)]
            proxy_count_dict[func_name] = len(proxy_list)
        except Exception as e:
            log.error(u"代理获取函数 {} 运行出错!".format(func_name))
            log.error(str(e))
    log.info(u"所有函数运行完毕 " + "***" * 5)
    for func_name, func in member_list:
        log.debug(u"函数: {n}, 获取到代理数: {c}".format(n=func_name, c=proxy_count_dict.get(func_name, 0)))


def checkSingleProxy(func):
    """
    检查指定的FetchFreeProxy某个function运行情况
    Args:
        func: FetchFreeProxy中某个可调用方法

    Returns:
        None
    """
    func_name = getattr(func, '__name__', "None")
    log.info("start running func: {}".format(func_name))
    count = 0
    for proxy in func():
        if verifyProxyFormat(proxy):
            log.debug("{} fetch proxy: {}".format(func_name, proxy))
            count += 1
    log.debug("{n} completed, fetch proxy number: {c}".format(n=func_name, c=count))


if __name__ == '__main__':
    # proxylistplus(FetchFreeProxy.proxylistplus)
    print(checkSingleProxy(FetchFreeProxy.coderbusy))
