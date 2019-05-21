#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import requests
import re
from bs4 import BeautifulSoup
from . import SpiderModel
from urllib.parse import quote


class TMGoodSpider():
    def __init__(self):
        self.__good_list = []
        self.__url = "https://list.tmall.com/search_product.htm?q="
        self.__real_url = None
        self.__headers = {
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko)',
            'authority': 'list.tmall.com',
            'method': 'GET',
            'path': '/search_product.htm?q=',
            'scheme': 'https'
        }

    def start(self, keyword):
        if len(keyword) > 0:
            if self.__get_goods(quote(keyword)):
                return self.__real_url, self.__good_list
            else:
                print('No Goods Get...')
                return None
        self.__headers['path'] += keyword

    def __get_goods(self, keyword):
        try:
            self.__real_url = self.__url + keyword
            res = requests.get(url=self.__real_url, headers=self.__headers, timeout=5)
            if res.status_code == 200:
                return self.__parser(res.text)
        except Exception as e:
            print(e.__str__())
            return False

    def __parser(self, parsercontent):
        soup = BeautifulSoup(parsercontent, 'lxml')
        for item in soup.select('.product-iWrap'):
            good_model = SpiderModel.GoodModel()
            good_model.platform = '2'
            good_model.title = item.select('.productTitle')[0].a.get('title')
            href = item.select('.productTitle')[0].a.get('href')
            id = re.findall(r'id=(\w+)&', href)[0]
            sellerid = re.findall(r'user_id=(\w+)&', href)[0]
            good_model.urls = r'https:' + href
            good_model.sellerid = sellerid
            good_model.id = id
            good_model.price = item.select('.productPrice')[0].text.strip()
            good_model.img = item.select('.productImg-wrap')[0].a.img.get('data-ks-lazyload')
            self.__good_list.append(good_model.load2json())
        return True


class TMCommentSpider():
    def __init__(self):
        self.__comments_list = []
        self.__itemid = None
        self.__sellerid = None
        self.__url = "https://rate.tmall.com/list_detail_rate.htm"
        self.__params = {
            'itemId': None,
            'sellerId': None,
            'order:': 3,
            'currentPage': 1
        }
        self.__headers = {

        }


if __name__ == '__main__':
    tm_spider = TMGoodSpider()
    url, good_list = tm_spider.start('python')
    for good in good_list:
        print(good.__str__())
    print(url)
    print(len(good_list))
