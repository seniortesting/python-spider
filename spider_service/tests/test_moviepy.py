import logging
import random
import unittest
import uuid
import datetime
from unittest import TestCase
from moviepy.editor import *

log = logging.getLogger(__name__)
consoleHandler = logging.StreamHandler()
consoleHandler.setLevel(logging.INFO)

log.setLevel(logging.DEBUG)
log.addHandler(consoleHandler)

'''
1. 安装moviepy
'''

class MoviePyTestCase(unittest.TestCase):

    def prepare_data(self):
        '''
        数据准备
        :return:
        '''
        self.__movies = [
            {'id': 1001,
             'name': '7+Mythical+Creatures+That+Existed+in+Real+Life',
             'path': 'D:\\自媒体\\7-Mythical-Creatures-That\\7+Mythical+Creatures+That+Existed+in+Real+Life.mp4',
             'duration': {'start': '00:00:05,791', 'end': '00:00:07,470', 'content': ''}
             },
            {'id': 1002,
             'name': '15-Most-Deadly-Eagle-Attacks-in-the-World',
             'path': 'D:\\自媒体\\7-Mythical-Creatures-That\\CCTV纪录-nvsSsLEB1y0.mp4',
             'duration': {'start': '00:00:20,791', 'end': '00:00:21,510', 'content': ''}
             },
            {'id': 1003,
             'name': '15-Strangest-Creatures-Recently-Discovered',
             'path': 'D:\\自媒体\\7-Mythical-Creatures-That\\FOR-HONOR-Full Movie-Cinematic-4K.webm',
             'duration': {'start': '00:00:23,401', 'end': '00:00:25,080', 'content': ''}
             },
            {'id': 1004, 'name': 'The-History-of-Speculative-Zoology',
             'path': 'D:\\自媒体\\7-Mythical-Creatures-That\\METRO-EXODUS-Full-Movie-Cinematic-4K-Trailers-a8iD3hs9dZs.webm',
             'duration': {'start': '00:00:52,981', 'end': '00:00:56,310', 'content': ''}
             },
            {'id': 1004, 'name': 'The-History-of-Speculative-Zoology',
             'path': 'D:\\自媒体\\7-Mythical-Creatures-That\\农历就是阴历吗-qXFeQmb2gU8.mp4',
             'duration': {'start': '00:01:52,981', 'end': '00:03:56,310', 'content': ''}
             },
        ]
        self.__factor = 3
        self.__second = 10

    def randomGroup(self, list, num):
        '''
        随机几个视频合并为一个小视频
        :param list:
        :param num:
        :return:
        '''
        random.shuffle(list)
        for i in range(0, len(list), num):
            yield list[i:i + num]

    def cacularDuration(self, start, end):
        '''
        通过给定的每个电影的开始和结束时间节点截取前后总共self.__second秒片段
        :param start:
        :param end:
        :return:
        '''
        start_time = datetime.datetime.strptime(start, '%H:%M:%S,%f')
        end_time = datetime.datetime.strptime(end, '%H:%M:%S,%f')
        # seconds = datetime.timedelta(hours=strtime.tm_hour, minutes=strtime.tm_min, seconds=strtime.tm_sec).total_seconds()
        total = (end_time - start_time).total_seconds()
        if total < self.__second:
            # 前后添加后为10秒
            left_seconds = self.__second - total
            each_second = left_seconds / 2
            start_time = start_time + datetime.timedelta(seconds=-each_second)
            end_time = end_time + datetime.timedelta(seconds=each_second)
        return (start_time, end_time)

    def test_clip(self):
        '''
         剪切，合并视频
        :return:
        '''
        self.prepare_data()
        movies = self.randomGroup(self.__movies, self.__factor)
        name = uuid.uuid4().hex
        # 截取片段
        for groupIndex, mGroup in enumerate(movies):
            # 每self.__factor个一组的
            outputName = '%s_%d.mp4' % (name, groupIndex)
            outputPath = '%s/%s' % ('D:\\自媒体', outputName)
            movielist = []
            startIndex = groupIndex + 1
            startTime = datetime.datetime.now()
            log.info('开始第%s个小视频制作，开始时间: %s', startIndex, startTime)
            for m in mGroup:
                # 参数
                if len(mGroup) == self.__factor:
                    path = m.get('path')
                    start = m.get('duration').get('start')
                    end = m.get('duration').get('end')
                    start_time, end_time = self.cacularDuration(start, end)
                    start_time_str = start_time.strftime('%H:%M:%S,%f')
                    end_time_str = end_time.strftime('%H:%M:%S,%f')
                    # 视频
                    videoClip = (VideoFileClip(path)
                                 .resize(height=360)
                                 .subclip(start_time_str, end_time_str))
                    movielist.append(videoClip)
            # Generate a text clip. You can customize the font, color, etc.
            # textClip = (TextClip("小视频编辑器", fontsize=70, color='white')
            #             .set_pos('center').set_duration(self.__second)
            #             )
            if len(movielist) == self.__factor:
                log.info('制作第%s个小视频，合并视频是: %s', startIndex, movielist)
                video = concatenate_videoclips(movielist, method='compose')
                # video = CompositeVideoClip(movielist + [textClip])
                video.write_videofile(outputPath)
                video.close()
                endTime = datetime.datetime.now()
                totalSeconds = (endTime - startTime).total_seconds()
                log.info('结束第%s个小视频制作，共计耗时: %s秒', startIndex, totalSeconds)

    def test_concat(self):
        '''
        拼接
        :return:
        '''
        pass

    def test_title(self):
        '''
        加上标题
        :return:
        '''
        pass
