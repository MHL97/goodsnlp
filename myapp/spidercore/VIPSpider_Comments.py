#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import requests
from bs4 import BeautifulSoup
import re
import json
import time
# import SpiderModel
from .SpiderModel import CommentModel


class VIPCommentsSpider():
    def __init__(self):
        self.__comments_list = []
        self.__headers = {
            'host': "detail.vip.com",
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko)',
        }
        self.com_model = CommentModel()

    def start(self, url, page):
        try:
            res = requests.get(url=url, headers=self.__headers, timeout=5)
            if res.status_code == 200:
                self.com_model.platform = '4'
                self.com_model.product_url = url
                soup = BeautifulSoup(res.text, 'lxml')
                self.com_model.img = soup.find_all('img', attrs={'class': 'slide-mid-pic lazy'})[0].get('data-original')
                title = soup.find_all('p', attrs={'class': 'pib-title-detail'})[0].get('title').strip()
                self.com_model.title = title
                spuid = re.findall(r'\"spuId\":\"(\w+)\",', res.text)[0]
                self.com_model.id = spuid
                brandid = url.split('-')[1]

                # 请求获取总的评价数量
                comm_num_url = "https://detail.vip.com/v2/mapi?_path=rest%2Fcontent%2Freputation%2FgetCountBySpuId"
                params = {
                    'spuId': spuid,
                    'brandId': brandid
                }
                comm_num_res = requests.get(url=comm_num_url, headers=self.__headers, params=params, timeout=3)
                json_text = comm_num_res.json()
                # print(json_text)
                # print(comm_num_url)
                count = json_text.get('data')
                self.com_model.all_num = count
                # print('vip-评论数量:', count)
                if int(page) > int(count) // 10:
                    print('页数过多!')
                    return None, None
                else:
                    for i in range(1, page + 1):
                        if not self.__get_comments(brandid, spuid, i):
                            return None, None
                        time.sleep(0.2)
                    return self.com_model.load2json(), list(set(self.__comments_list))
            else:
                return None, None
        except Exception as e:
            print('VIP COMMENTS START ERROR:', e.__str__())
            return None, None

    def __get_comments(self, brandid, spuid, page):
        url = "https://detail.vip.com/v2/mapi?_path=rest%2Fcontent%2Freputation%2FqueryBySpuId"
        params = {
            'page': page,
            'pageSize': '10',
            'spuId': spuid,
            'brandId': brandid
        }
        try:
            res = requests.get(url=url, headers=self.__headers, params=params, timeout=5)
            if res.status_code == 200:
                json_text = json.loads(res.text.encode('utf8').decode('utf8'))
                for item in json_text['data']:
                    item_txt = item['reputation']['content'].replace('\n', '')
                    if len(item_txt) > 20:
                        self.__comments_list.append(item_txt)
                return True
        except Exception as e:
            print('VIP COMMENTS GET ERROR:', e.__str__())
            return False
        pass


if __name__ == '__main__':
    st = time.time()
    url = " https://detail.vip.com/detail-3131512-572555443.html"
    sn_comm_spider = VIPCommentsSpider()
    model, comm_list = sn_comm_spider.start(url=url, page=1)
    print(model.__str__())
    if model is not None and comm_list is not None:
        for item in comm_list:
            print(item)
        et = time.time()
        print(len(comm_list))
        print('Spend time:', et - st)
