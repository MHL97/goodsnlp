#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import time

# import JDSpider_Goods
# import TMSpider_Goods
# import SNSpider_Goods
# import VIPSpider_Goods

from . import JDSpider_Goods
from . import TMSpider_Goods
from . import SNSpider_Goods
from . import VIPSpider_Goods

from . import VIPSpider_Comments
from . import SNSpider_Comments
from . import JDSpider_Comments
from .SpiderModel import CommentModel

from selenium import webdriver

class Spiders():
    def __init__(self):
        self.comments_url_templates = {
            'detail.vip.com': 'vip',
            'product.suning.com': 'sn',
            'item.jd.com': 'jd'
        }
        self.com_model = None
        self.result = []
        pass

    def do_ajax(self):
        driver = webdriver.PhantomJS()
        driver.get(url)
        # 切换到内容的frame
        driver.switch_to_frame("contentFrame")
        data = driver.find_element_by_id("m-pl-container").find_elements_by_tag_name("li")
        for i in range(len(data)):
            nb = data[i].find_element_by_class_name("nb").text
            if '万' in nb and int(nb.split("万")[0]) > 100:
                msk = data[i].find_element_by_css_selector("a.msk")
        # 定位到下一页的url
        url = driver.find_element_by_css_selector('a.zbtn.znxt').get_attribute('href')

    def start_comments(self, product_url, page):
        for k, v in self.comments_url_templates.items():
            if k in product_url:
                if v == 'vip':
                    self.com_model, self.result = VIPSpider_Comments.VIPCommentsSpider().start(product_url, page)
                elif v == 'sn':
                    self.com_model, self.result = SNSpider_Comments.SNCommentsSpider().start(product_url, page)
                elif v == 'jd':
                    self.com_model, self.result = JDSpider_Comments.JDCommentSpider().start(product_url, page)
        return self.com_model, self.result

    def start_goods(self, keyword):
        jd_spider = JDSpider_Goods.JDGoodSpider()
        tm_spider = TMSpider_Goods.TMGoodSpider()
        sn_spider = SNSpider_Goods.SNGoodSpider()
        vip_spider = VIPSpider_Goods.VIPGoodSpider()

        jd_url, jd_list = jd_spider.start(keyword, page=1)
        # tm_url, tm_list = tm_spider.start(keyword)
        sn_url, sn_list = sn_spider.start(keyword)
        vip_url, vip_list = vip_spider.start(keyword)

        result = {}
        result['jd'] = {'url': jd_url, 'result': jd_list}
        # result['tm'] = {'url': tm_url, 'result': tm_list}
        result['sn'] = {'url': sn_url, 'result': sn_list}
        result['vip'] = {'url': vip_url, 'result': vip_list}
        print('Spider key:', keyword)
        print('jd:', len(jd_list), ' url', jd_url)
        # print('tm:', len(tm_list), ' url', tm_url)
        print('sn:', len(sn_list), ' url', sn_url)
        print('vip:', len(vip_list), ' url', vip_url)
        return result

if __name__ == '__main__':
    st = time.time()
    spider = SpiderHelper()
    spider.start_goods('python')
    et = time.time()
    print(et - st)
