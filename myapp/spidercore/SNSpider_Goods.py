#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import requests
from bs4 import BeautifulSoup
from . import SpiderModel
from urllib.parse import quote
import re


class SNGoodSpider():
    """
    抓取苏宁易购的商品搜索结果
    """

    def __init__(self):
        self.__goods_list = []
        self.__root = "http://search.suning.com/"
        self.__real_url = None
        self.__headers = {
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko)',
            'method': 'GET',
            'host': 'search.suning.com',
        }

    def start(self, keyword):
        """

        :param keyword: 搜索关键字
        :return: model的结果集
        """
        if self.__get_goods(quote(keyword)):
            print('sn:', self.__goods_list)
            return self.__real_url, self.__goods_list
        else:
            return None, None

    def __get_goods(self, keyword):
        self.__real_url = self.__root + keyword + '/'
        res = requests.get(url=self.__real_url, headers=self.__headers, timeout=5)
        # print(res.url)
        if res.status_code == 200:
            # print(res.encoding)
            return self.__parser(res.text)

    def __parser(self, parsercontent):
        soup = BeautifulSoup(parsercontent, 'lxml')
        try:
            for item in soup.select('.item-bg'):
                good_model = SpiderModel.GoodModel();
                good_model.platform = '3'
                good_model.img = item.select('.img-block')[0].a.img.get('src')
                good_model.price = item.select('.price-box')[0].span.text.strip()
                href = item.select('.img-block')[0].a.get('href')
                id = re.findall(r'/(\w+).html', href)[0]
                sellid = re.findall(r'/(\w+)/', href)[0]
                good_model.urls = 'http:' + href
                good_model.id = id
                good_model.sellerid = sellid
                good_model.title = item.select('.title-selling-point')[0].a.get('title')
                self.__goods_list.append(good_model.load2json())
                return True
        except Exception as e:
            print('Error in SN_Goods:', e.__str__())
            return False



if __name__ == '__main__':
    sn_spider = SNGoodSpider()
    url, good_list = sn_spider.start('电脑')
    for good in good_list:
        print(good.__str__())
    print(len(good_list))
    print(url)
