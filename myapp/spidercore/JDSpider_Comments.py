#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from bs4 import BeautifulSoup
import requests
import json
import time
import threading
import re
# import SpiderModel
from .SpiderModel import CommentModel


# 包装线程类，实现多线程
class SpiderThread(threading.Thread):
    def __init__(self, func, args=()):
        threading.Thread.__init__(self)
        self.result = None
        self.args = args
        self.func = func
        self.end = False

    def run(self):
        time.sleep(0.5)
        self.result = self.func(*self.args)
        if self.result is None:
            self.end = True

    def get_result(self):
        threading.Thread.join(self)
        try:
            return self.result
        except threading.ThreadError as e:
            print('Thread Error!' + e.__str__())
            return None


class JDCommentSpider:
    def __init__(self):
        self.__comments_list = []
        self.__product_url = None
        self.__product_id = None
        self.com_model = CommentModel()

    def get_info(self, url, product_id):
        headers = {
            'authority': 'item.jd.com',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
                          ' (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36',
            'path': '/' + product_id + '.html'
        }
        try:
            res = requests.get(url, headers=headers, timeout=5)
            soup = BeautifulSoup(res.text, 'lxml')
            img_src = ''
            tag_img = soup.find_all('img', attrs={'class': 'img-hover'})

            tag_li = soup.find_all('li', attrs={'class': 'img-hover'})

            if len(tag_img) > 0:
                img_src = tag_img[0].get('src')
            elif len(tag_li) > 0:
                img_src = tag_li[0].img.get('src')

            sorts_name = soup.find_all('div', attrs={'class': 'item first'})[0].text.strip()
            title = soup.find_all('div', attrs={'class': 'sku-name'})[0].text.strip()
            return img_src, sorts_name, title
        except Exception as e:
            print('JD get info error:', e.__str__())
            return None, None, None

    def start(self, product_url, page):
        self.__product_url = product_url
        self.com_model.product_url = product_url
        self.com_model.platform = '1'
        self.__product_id = re.findall(r'/(\d+).html', product_url)[0]
        self.com_model.id = self.__product_id
        self.com_model.img, self.com_model.sorts_name, self.com_model.title = self.get_info(url=self.__product_url,
                                                                                            product_id=self.__product_id)
        if self.__product_id is not None:
            n = 1
            while n <= page:
                spider = SpiderThread(func=self.__get_comments, args=(self.__product_id, n))
                n += 1
                spider.run()
                if spider.end:
                    break
                else:
                    self.__parser(spider.result)
            return self.com_model.load2json(), list(set(self.__comments_list))
        return None, None

    def __get_comments(self, productid, page):
        url = "http://sclub.jd.com/comment/productPageComments.action?"  # 请求的根url

        header = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
                          ' (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36',
            'referer': self.__product_url
        }
        params = {
            'callback': 'fetchJSON_comment320203',  # using this value temporarily, can modify number
            'productId': productid,
            'score': 0,
            'sortType': 5,
            'page': page,
            'pageSize': 10,
            'isShadowSku': 0,
            'fold': 1,
        }

        res = requests.get(url, headers=header, params=params)

        # 200 ok
        if res.status_code == 200:
            soup = BeautifulSoup(res.content, 'lxml')
            # 截取json部分并格式化json格式, 同时捕获异常
            try:
                json_obj = json.loads(res.text[24: -2])
                self.com_model.good_rote = json_obj['productCommentSummary']['goodRateShow']  # 好评率
                self.com_model.good_num = json_obj['productCommentSummary']['goodCountStr']  # 好评数
                self.com_model.all_num = json_obj['productCommentSummary']['commentCountStr']  # 评论总数
                self.com_model.mid_num = json_obj['productCommentSummary']['generalCountStr']  # 中评数
                self.com_model.poor_num = json_obj['productCommentSummary']['poorCountStr']  # 差评数
                if json_obj['comments']:
                    return json_obj['comments']
            except json.decoder.JSONDecodeError as e:
                print(res.url)
                print('Oh mo god! IP Banned:' + e.__str__())
                return None
        else:
            print('网站响应失败:', res.url)
            return None

    def __parser(self, json_list):
        if len(json_list) > 0:
            for comm in json_list:
                comm_str = comm.get('content').replace('\n', '')
                if len(comm_str) > 20:
                    self.__comments_list.append(comm_str)
        return True


if __name__ == '__main__':
    # 7612626 id
    st = time.time()
    url = "https://item.jd.com/12451724.html"
    jd_spider = JDCommentSpider()
    jd_spider.get_info(url, '12451724')
    # model, comm_list = jd_spider.start(product_url=url, page=1)
    # # seconde arg  is best not be more than 50. （10*50）
    # # jd_good = start(7341442, 1)
    # end = time.time()
    # print('程序耗时：', end - st)
    # # print('好评数：', jd_good.good_comm_num)
    # # print('差评数：', jd_good.poor_comm_num)
    # # print('中评数：', jd_good.mid_comm_num)
    # # print('好评率：', jd_good.good_rote)
    # # print('评论总数：', jd_good.comment_num)
    # # print('评论列表：', jd_good.comm_list)
    # # print(len(jd_good.comm_list))
    # print(model.__str__())
    # for item in comm_list:
    #     print(item)
    # write2file(jd_good.comm_list)
