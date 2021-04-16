# -*- coding:utf-8 -*-
import random
import time

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys

from app.api.util.web_request import WebRequest, USER_AGENT_PC, USER_AGENT_MOBILE


class SpiderWebDriver(object):

    def __init__(self, url: str,
                 userAgent: str = None,referer: str=None, proxy: str = None):
        # 进入浏览器设置
        chrome_options = Options()
        # 配置参数: http://chromedriver.chromium.org/capabilities
        # 详细参数： https://peter.sh/experiments/chromium-command-line-switches/
        chrome_options.add_argument('lang=zh_CN.UTF-8')
        # chrome_options.add_argument('headless')
        # chrome_options.add_argument('window-size=1024,768')
        chrome_options.add_argument('no-sandbox')
        chrome_options.add_argument("disable-gpu")
        chrome_options.add_argument("ignore-certificate-errors");
        chrome_options.add_argument("disable-popup-blocking");
        chrome_options.add_argument("disable-default-apps");
        # Chrome is being controlled by automated test software

        if userAgent is None:
            # 默认safari pc端浏览器
            userAgent = 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/534.57.2 (KHTML, like Gecko) Version/5.1.7 Safari/534.57.2'
        chrome_options.add_argument('user-agent="' + userAgent + '"')
        chrome_options.add_argument('referer="https://www.google.com/"')
        if proxy is not None:
            proxy_str = "http://{proxy}".format(proxy=proxy)
            chrome_options.add_argument('proxy-server=' + proxy_str)
        # http://chromedriver.storage.googleapis.com/index.html
        self.driver = webdriver.Chrome(options=chrome_options)
        self.driver.maximize_window()
        if url:
            self.driver.get(url=url)

    def close(self):
        driver = self.driver
        if driver is None:
            return
        try:
            driver.close()
            driver.quit()
        finally:
            self.driver = None

    def __enter__(self):
        return self

    def __exit__(self, *exc_info):
        del exc_info
        self.close()

    def open(self, url):
        self.driver.get(url)

    def get_cookies(self):
        cookies_dict = {}
        cookies = self.driver.get_cookies()
        for cookie in cookies:
            cookies_dict[cookie['name']] = cookie['value']
        return cookies_dict

    def execute_js(self, js, *args):
        return self.driver.execute_script(js, args)


def adsenseClick():
    # 获取wordpress的随机文章
    url = 'https://pingbook.top/wp-json/wp/v2/posts'
    r=WebRequest()
    post_list=r.pc().get(url=url).json()
    # links=[ item.get('link') for item in post_list]
    # print(links)
    # post_list =[{'link': 'https://pingbook.top/vue-videojs-m3u8-player-a-html5-video-player/'}]
    # 模拟操作打开文章
    proxyset = set()
    for num in range(10000):
        post=random.choice(post_list)
        post_url=post.get('link')
        print('发送请求的文章地址是: {}'.format(post_url))
        agents = USER_AGENT_PC + USER_AGENT_MOBILE
        time_count = num + 1
        driver = None
        try:
            content = r.pc().get('https://open.pingbook.top/proxy/get?type=valid').json()
            proxy = content.get('data').get('proxy')
            print('发送请求的代理是: {}'.format(proxy))
            if proxy not in proxyset:
                # 时候重复的使用了相同的ip地址
                proxyset.add(proxy)
                agent = random.choice(agents)
                driver = SpiderWebDriver(post_url, agent, proxy)
                driver.open(post_url)
                print('已经打开博客地址: {}'.format(post_url))
                driver.driver.refresh()
                submitBtn =driver.driver.find_element_by_id('submit')
                if submitBtn:
                    # 滚动到对应的广告部分
                    driver.driver.execute_script('arguments[0].scrollIntoView(true);',submitBtn)
                    submitBtn.click()
                    time.sleep(3)
                    # driver.driver.refresh()
                    # wait = WebDriverWait(driver.driver, 6)
                    # element = wait.until(expected_conditions.element_to_be_clickable((By.ID, 'ads')))

                    # driver.close()
                    print('第{}次轮训成功,代理: {}。。。。'.format(time_count, proxy))

                # actionBtn = driver.driver.find_element_by_class_name('copy-btn')
                # if actionBtn:
                #     driver.driver.refresh()
                #     wait = WebDriverWait(driver.driver, 6)
                #     element = wait.until(expected_conditions.element_to_be_clickable((By.ID, 'ads')))
                #     actionBtn.click()
                #     driver.close()
                #     print('第{}次轮训成功,代理: {}。。。。'.format(time, proxy))
            else:
                print('当前代理地址: {}已经存在,不再使用该地址进行测试,代理池大小: {}!'.format(proxy,len(proxyset)))
        except Exception as e:
            print('第{}次轮训失败,失败信息: {}。。。。'.format(time_count, e))
            # raise
        finally:
            if driver is not None:
                driver.close()


def searchGoogle():
    keyword= 'nuxt create nuxt app error :pingbook.top'
    # 模拟操作打开文章
    proxyset = set()
    r=WebRequest()
    agents=USER_AGENT_PC
    for num in range(10000):
        driver = None
        try:
            content = r.pc().get('https://open.pingbook.top/proxy/get?type=valid').json()
            proxy = content.get('data').get('proxy')
            print('发送请求的代理是: {}'.format(proxy))
            if proxy not in proxyset:
                # 时候重复的使用了相同的ip地址
                proxyset.add(proxy)
                agent = random.choice(agents)
                spider = SpiderWebDriver(None, agent, proxy)
                spider.open('https://google.com')
                driver =spider.driver
                # 输入关键字
                inputbox=driver.find_element_by_name('q')
                if inputbox:
                    inputbox.send_keys(keyword)
                    inputbox.send_keys(Keys.ENTER)
                    time.sleep(3)
                    # 点击第一条记录
                    first_record=driver.find_element_by_css_selector('#rso > div:nth-child(1) > div > div:nth-child(1) > div > div > div.r > a')
                    first_record.click()
                    time.sleep(5)
                    driver.refresh()
                    time.sleep(6)
        except Exception as e:
            print('第{}次轮训失败,失败信息: {}。。。。'.format(num, e))
        finally:
            if driver is not None:
                driver.quit()





if __name__ == '__main__':
   adsenseClick()
