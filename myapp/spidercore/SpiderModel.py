#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import json


class CommentModel():
    def __init__(self):
        self.product_url = None
        self.title = ''
        self.id = None
        self.all_num = 0
        self.good_rote = 0
        self.good_num = 0
        self.mid_num = 0
        self.poor_num = 0
        self.img = None
        self.platform = ''
        self.sorts_name = ''

    def __str__(self):
        return  '商品链接:%s\n图片路径:%s\n评论总数:%s\n好评数量:%s\n中评数量:%s\n差评数量:%s\n好评率:%s\n------\n' % (
            self.product_url, self.img, self.all_num, self.good_num, self.mid_num, self.poor_num, self.good_rote
        )

    def load2json(self):
        dic = {}
        sorts_id = 9
        dic['product_url'] = self.product_url
        dic['product_title'] = self.title
        dic['total_num'] = self.all_num
        dic['good_num'] = self.good_num
        dic['mid_num'] = self.mid_num
        dic['poor_num'] = self.poor_num
        dic['good_rote'] = self.good_rote
        dic['img_url'] = self.img
        dic['platform_id'] = self.platform
        dic['product_id'] = self.id
        if '电器' in self.sorts_name:
            sorts_id = 1
        elif '书' in self.sorts_name:
            sorts_id = 2
        elif '家具' in self.sorts_name:
            sorts_id = 3
        elif '服' in self.sorts_name:
            sorts_id = 4
        elif '食' in self.sorts_name:
            sorts_id = 5
        elif '药' in self.sorts_name:
            sorts_id = 6
        elif '电脑' in self.sorts_name or '码' in self.sorts_name or '手机' in self.sorts_name:
            sorts_id = 7
        elif '肤' in self.sorts_name:
            sorts_id = 8
        dic['sorts_id'] = sorts_id
        return dic


class GoodModel():
    def __init__(self):
        self.title = None
        self.price = None
        self.img = None
        self.urls = None
        self.id = None
        self.sellerid = None
        self.platform = ''

    def __str__(self):
        return "id:%s\n名称:%s\n价格:%s\n图片路径:%s\n商品链接:%s\n商家ID:%s\n------\n" % (
            self.id, self.title, self.price, self.img, self.urls, self.sellerid
        )

    def load2json(self):
        dic = {}
        dic['id'] = self.id
        dic['title'] = str(self.title)
        dic['price'] = self.price
        dic['img'] = self.img
        dic['href'] = self.urls
        dic['sellerid'] = self.sellerid
        dic['platform'] = self.platform
        return dic
