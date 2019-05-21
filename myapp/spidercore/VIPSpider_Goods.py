#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# from bs4 import BeautifulSoup
import requests
import re
from urllib.parse import quote
import json
from . import SpiderModel


class VIPGoodSpider():
    def __init__(self):
        self.__goods_list = []
        self.__url = "https://category.vip.com/suggest.php?keyword="
        self.__real_url = None
        self.__headers = {
            'host': "category.vip.com",
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko)'
        }

    def __get_goods(self, keyword):
        self.__real_url = self.__url + keyword
        try:
            res = requests.get(url=self.__real_url, headers=self.__headers, timeout=5)
            if res.status_code == 200:
                # print(res.text)

                js_text = re.findall(r"\"products\":(\[.*\])", res.text)[0]
                json_info = json.loads(js_text)
                for item in json_info:
                    good_model = SpiderModel.GoodModel()
                    good_model.platform = '4'
                    good_model.title = item.get('product_name')
                    good_model.price = item.get('promotionPrice')
                    good_model.id = item.get('product_id')
                    good_model.img = item.get('small_image')
                    good_model.sellerid = item.get('brand_id')
                    good_model.urls = "https://detail.vip.com/detail-%s-%s.html" % (
                        item.get('brand_id'), item.get('product_id'))
                    self.__goods_list.append(good_model.load2json())
                return True
        except Exception as e:
            print('Req Error:', e.__str__())
            return False

    def start(self, keyword):
        if len(keyword) > 0:
            if self.__get_goods(quote(keyword)):
                return self.__real_url, self.__goods_list
        else:
            return None


if __name__ == '__main__':
    wph_spider = VIPGoodSpider()
    url, good_list = wph_spider.start('衣服')
    for item in good_list:
        print(item.__str__())
    print(url)
    print(len(good_list))
