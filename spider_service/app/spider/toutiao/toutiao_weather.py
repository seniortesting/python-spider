# -*- coding:utf-8 -*-
import logging

from app.api.util.web_request import WebRequest

logging.basicConfig(level=logging.INFO,
                    format='[%(asctime)s.%(msecs).03d - %(filename)s:%(lineno)d %(levelname)s]: %(message)s')
log = logging.getLogger(__name__)

WEATHER_URL = 'https://www.toutiao.com/stream/widget/local_weather/data/'


class ToutiaoWeather(object):
    def __init__(self):
        self.http = WebRequest()

    def weather(self, city):
        '''
        得到天气预报情况
        :param city:
        :return:
        '''
        params = {
            city: city
        }
        headers = {
            'content-type': 'application/x-www-form-urlencoded',
            'referer': 'https://www.toutiao.com/ch/news_hot/'
        }
        response = self.http.pc().get(WEATHER_URL, params=params, headers=headers)
        response.encoding = 'utf-8'
        result = response.json()
        return result


if __name__ == '__main__':
    weather = ToutiaoWeather()
    result = weather.weather('上海')
    print(result)
