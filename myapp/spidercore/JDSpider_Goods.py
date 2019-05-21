#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from urllib.parse import quote
import requests
from bs4 import BeautifulSoup
from time import time
import re
from . import SpiderModel


class JDGoodSpider():
    def __init__(self):
        self.goods_list = []
        self.first_root = ""
        self.last_root = ""
        self.cur_page = 0
        self.__real_url = None

    def __get_first30(self, keyword, page):
        """
        获取前30条记录
        :param keyword: 搜索关键字
        :param page: 奇数页码
        :return: show_items or None
        """
        self.cur_page = page
        top30_url = "https://search.jd.com/Search?enc=utf-8&qrst=1&rt=1" \
                    "&keyword=%s" \
                    "&page=%s" % (quote(keyword), page)
        self.first_root = top30_url
        headers = {
            'authority': 'search.jd.com',
            'method': 'GET',
            'path': top30_url,
            'scheme': 'https',
            'user-agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko)'
                          ' Chrome/66.0.3359.139 Safari/537.36',
            'referer': "https://search.jd.com/",
        }
        try:
            self.__real_url = top30_url
            res = requests.get(url=top30_url, headers=headers, timeout=5)
            if res.status_code == 200:
                res_content = res.text.encode(res.encoding).decode('utf8')
                return self.__parser(res_content)
        except Exception as e:
            print(e.__str__())
            return None

    def __get_last30(self, keyword, page, s, show_items):
        """
        获取后30条记录
        :param keyword: 搜索关键字
        :param page: 偶数页码
        :param s: 商品数量，自动构造
        :param show_items: 前30条商品记录的id
        :return: True or False
        """
        self.cur_page = page
        last30_url = "https://search.jd.com/s_new.php??enc=utf-8&qrst=1&rt=1&scrolling=y" \
                     "&keyword=%s" \
                     "&page=%s" \
                     "&s=%s" \
                     "&show_items=%s" \
                     "&log_id=%s" % (keyword, page, s, show_items, '%.5f' % time())
        self.last_root = last30_url
        headers = {
            'authority': 'search.jd.com',
            'method': 'GET',
            'path': last30_url,
            'referer': self.first_root,
            'scheme': 'https',
            'user-agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.139 Safari/537.36',
            'x-requested-with': 'XMLHttpRequest',
        }
        # try:
        res = requests.get(url=last30_url, headers=headers, timeout=5)
        if res.status_code == 200:
            res_content = res.text.encode(res.encoding).decode('utf8')
            self.__parser(res_content)
            return True
        # except Exception as e:
        #     print(e.__str__())
        return False

    def start(self, keyword, page):
        """
        京东商品信息爬虫入口
        :param keyword: 搜索关键字
        :param page: 页数，每页默认60条记录
        :return: 商品模型列表
        """
        if int(page) > 0:
            show_items = self.__get_first30(keyword=keyword, page=(2*int(page)-1))
            self.__get_last30(keyword=keyword, page=2*int(page), s=83, show_items=show_items)
            # print('jd:', self.goods_list)
            return self.__real_url, self.goods_list
        else:
            return False

    def __parser(self, parser_content):
        """
        内容解析模块
        :param parser_content:待解析的网页响应内容
        :return: 前30条商品的id字符串，用于请求后30条记录
        """
        show_items = None
        soup = BeautifulSoup(parser_content, 'lxml')
        good_list = []
        show_items_id = []
        for item in soup.select('.gl-i-wrap'):
            temp_model = SpiderModel.GoodModel()
            temp_model.platform = '1'
            temp_model.title = item.select('.p-name')[0].em.text.strip()
            temp_model.price = item.select('.p-price')[0].i.text.strip()
            temp_model.img = item.select('.p-img')[0].a.img.get('source-data-lazy-img')
            href = item.select('.p-img')[0].contents[1]['href']
            urls = ''
            if 'http' in href or 'https' in href:
                urls = href
            else:
                urls = r'http:' + href
            id = re.findall(r'(\w+).html', href)[0]
            temp_model.urls = urls
            temp_model.id = id
            good_list.append(temp_model.load2json())
            if divmod(self.cur_page, 2)[1] == 1:
                # 前30条都是奇数页码，此时需要获取id，请求后30条
                show_items_id.append(id)
        self.goods_list.extend(good_list)
        return ','.join(show_items_id)


if __name__ == '__main__':
    # ids = '12458274,11993134,12451724,12279949,11936238,12468732,12353915,11943853,12512461,12452929,12398725,12456107,12372646,12186192,12333540,12492797,12409581,12335366,12004711,11598704,12513158,12392747,12403048,12425597,11821937,12445029,12397576,11896415,12461168,12273412'
    jd_good_spider = JDGoodSpider()
    url, good_list = jd_good_spider.start('python', 1)
    for model in good_list:
        print(model.__str__())
    print(url)
    print(len(good_list))
