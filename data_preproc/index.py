#!/usr/bin/env python
# -*- coding:utf-8 -*-

import os
import re
import urllib
import json
import socket
import urllib.request
import urllib.parse
import urllib.error
# 设置超时
import time
import argparse

timeout = 5
socket.setdefaulttimeout(timeout)


class Crawler:
    # 睡眠时长
    __time_sleep = 0.1
    __amount = 0
    __start_amount = 0
    __counter = 0
    __s_dir = "result"
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:23.0) Gecko/20100101 Firefox/23.0'}

    # 获取图片url内容等
    # t 下载图片时间间隔
    def __init__(self, t=0.1):
        self.time_sleep = t

    # 保存图片
    def __save_image(self, rsp_data, word):

        if not os.path.exists("./" + self.__s_dir):
            os.mkdir("./" + self.__s_dir)
        # 判断名字是否重复，获取图片长度
        self.__counter = len(os.listdir('./' + self.__s_dir)) + 1
        now = 0
        for image_info in rsp_data['imgs']:
            if now >= 200:
                break
            try:
                time.sleep(self.time_sleep)
                fix = self.__get_suffix(image_info['objURL'])
                urllib.request.urlretrieve(image_info['objURL'], './' + self.__s_dir + '/' + str(self.__counter) + str(fix))
            except urllib.error.HTTPError as urllib_err:
                print(urllib_err)
                continue
            except Exception as err:
                time.sleep(1)
                print(err)
                print("error")
                continue
            else:
                print("now, " + str(self.__counter) + " images")
                self.__counter += 1
                now += 1
        return

    # 获取后缀名
    @staticmethod
    def __get_suffix(name):
        m = re.search(r'\.[^\.]*$', name)
        if m.group(0) and len(m.group(0)) <= 5:
            return m.group(0)
        else:
            return '.jpeg'

    # 获取前缀
    @staticmethod
    def __get_prefix(name):
        return name[:name.find('.')]

    # 开始获取
    def __get_images(self, word='apple'):
        search = urllib.parse.quote(word)
        # pn int 图片数
        pn = self.__start_amount
        pn = 0;
        while pn < self.__amount:

            url = 'http://image.baidu.com/search/avatarjson?tn=resultjsonavatarnew&ie=utf-8&word=' + search + '&cg=girl&pn=' + str(
                pn) + '&rn=60&itg=0&z=0&fr=&width=&height=&lm=-1&ic=0&s=0&st=-1&gsm=1e0000001e'
            # 设置header防ban
            try:
                time.sleep(self.time_sleep)
                req = urllib.request.Request(url=url, headers=self.headers)
                page = urllib.request.urlopen(req)
                rsp = page.read().decode('unicode_escape')
            except UnicodeDecodeError as e:
                print(e)
                print('-----UnicodeDecodeErrorurl:', url)
            except urllib.error.URLError as e:
                print(e)
                print("-----urlErrorurl:", url)
            except socket.timeout as e:
                print(e)
                print("-----socket timout:", url)
            else:
                # 解析json
                rsp_data = json.loads(rsp)
                self.__save_image(rsp_data, word)
                # 读取下一页
                print("next page")
                pn += 60
            finally:
                page.close()
        print("done")
        return

    def start(self, word, w_dir, spider_page_num=1, start_page=1):
        """
        爬虫入口
        :param word: 抓取的关键词
        :param spider_page_num: 需要抓取数据页数 总抓取图片数量为 页数x60
        :param start_page:起始页数
        :return:
        """
        self.__start_amount = (start_page - 1) * 60
        # self.__amount = 10 + self.__start_amount
        self.__amount = 300
        self.__s_dir = w_dir
        self.__get_images(word)


if __name__ == '__main__':

    ap = argparse.ArgumentParser()
    ap.add_argument("-w", "--word", required=True, help="search word")
    ap.add_argument("-d", "--dir", required=True, help="save dir")

    args = vars(ap.parse_args())

    s_dir = args['dir']
    s = args['word']
    crawler = Crawler(0.05)
    crawler.start(s.encode('utf-8'),s_dir,4,1)
