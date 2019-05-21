#!/usr/bin/env python3
# -*- coding: utf-8 -*-


import requests
from bs4 import BeautifulSoup
import time
import re
# import SpiderModel
from .SpiderModel import CommentModel


class SNCommentsSpider():
    """
    抓取苏宁易购的商品评论
    """

    def __init__(self):
        self.__headers = {
            'host': 'review.suning.com',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko)'
        }
        self.__comments_list = []
        self.com_model = CommentModel()

    def start(self, url, page):
        """
        开始评论抓取
        :param url:商品url
        :param page: 页数
        :return: 评论列表
        """
        res = requests.get(url=url, timeout=5)
        if res.status_code == 200:
            self.com_model.platform = '3'
            self.com_model.product_url = url
            self.com_model.id = re.findall(r'/(\d+).html', url)[0]
            soup = BeautifulSoup(res.text.encode(res.encoding).decode('utf-8'), 'lxml')
            # 从商品页中提取全部评论的链接，后续访问该链接抓取评论
            href = soup.select('#appraise')[0].a.get('href')
            title = soup.select('#itemDisplayName')[0].text.strip()
            self.com_model.sorts_name = soup.select('#category1')[0].text.strip()
            self.com_model.title = title
            real_url = str(href).split('-')

            for i in range(1, int(page) + 1):
                if self.__get_comments(real_url, i):
                    time.sleep(0.2)
                else:
                    return None, None
        return self.com_model.load2json(), list(set(self.__comments_list))

    def __get_comments(self, real_url, page):
        """
        获取评论文本
        :param real_url: 评论信息的真是url
        :param page:页数
        :return:T or F
        """
        real_url[-2] = str(page)
        url = '-'.join(real_url)
        try:
            res = requests.get(url='http:' + url, headers=self.__headers, timeout=5)
            if res.status_code == 200:

                soup = BeautifulSoup(res.text, 'lxml')
                self.com_model.sorts_name = soup.find_all('a', attrs={'id': 'category1'})[0].text.strip()

                self.com_model.img = soup.find_all('div', attrs={'class': 'the-pro-pic'})[0].a.img.get('src')
                self.com_model.all_num = soup.find_all('li', attrs={'data-type': 'total'})[0].get('data-num')

                self.com_model.good_num = soup.find_all('li', attrs={'data-type': 'good'})[0].get('data-num')
                self.com_model.mid_num = soup.find_all('li', attrs={'data-type': 'normal'})[0].get('data-num')
                self.com_model.poor_num = soup.find_all('li', attrs={'data-type': 'bad'})[0].get('data-num')
                self.com_model.good_rote = round(int(self.com_model.good_num) / int(self.com_model.all_num), 2) * 100
                for item in soup.select('.body-content'):
                    if len(item.text.strip()) > 20:
                        self.__comments_list.append(item.text.strip())
                return True
        except Exception as e:
            print('苏宁易购：该商品抓取失败！')
            return False


if __name__ == '__main__':
    goods_url = 'https://product.suning.com/0000000000/624041044.html?'
    page = 1
    sn_comm_spider = SNCommentsSpider()
    model, comm_list = sn_comm_spider.start(url=goods_url, page=page)
    print('抓取的评论数量：', len(comm_list))
