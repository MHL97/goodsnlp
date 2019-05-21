#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import jieba
import jieba.analyse
from snownlp import SnowNLP
import emoji
from . import DataVisual
from ..models import Comments

jieba.analyse.set_stop_words('static/corpus/stopwords.txt')
class NLPHelper():
    def __init__(self):
        pass

    def list2dict(self, old_list):
        i = 0
        new_dict = {}
        for item in old_list:
            new_dict[i] = item
            i += 1
        return new_dict

    def start(self,product_url, product_id, platform_id, comments_dict):
        stopwords = []
        with open('static/corpus/stopwords.txt', 'r', encoding='utf8') as f:
            for line in f.readlines():
                stopwords.append(line.strip('\n'))

        score_dict = {}  # 情感得分
        tf_idf_dict = {}  # 关键字
        sent_sort_dict = {} # 情感定位集合 是否是积极的
        new_text_dict = {}
        for k, v in comments_dict.items():
            new_text_dict[k] = jieba.cut(v)
        # k:index, v:content
        for k, v in comments_dict.items():
            tf_idf_dict[k] = jieba.analyse.extract_tags(v, topK=10)
            score_dict[k] = SnowNLP(v).sentiments

        result, sent_sort_dict = DataVisual.start_analysis(platform_id=platform_id,
                                           product_id=product_id,
                                           score_dict=score_dict,
                                           all_sentence_dict=comments_dict,
                                           tf_idf_dict=tf_idf_dict)
        if result is not None and sent_sort_dict is not None:
            print('正在保存评论信息：')
            try:
                for k, v in comments_dict.items():
                    new_text = ''
                    new_text_list = list(set(new_text_dict.get(k)))
                    for item in new_text_list:
                        if item not in stopwords:
                            new_text =  new_text +'/' + item
                    if len(new_text) > 255:
                        new_text = new_text[0:255]
                    if len(v) > 255:
                        v = v[0:255]
                    old_text = emoji.demojize(v)
                    if len(old_text) > 255:
                        old_text =  old_text[0:255]
                    comm_model = Comments()
                    comm_model.product_id = product_id
                    comm_model.product_url = product_url
                    comm_model.old_text = old_text
                    comm_model.new_text = emoji.demojize(new_text)
                    comm_model.key_words = '-'.join(tf_idf_dict.get(k))
                    comm_model.sent_score = score_dict.get(k)
                    comm_model.is_post = sent_sort_dict.get(k)
                    comm_model.save()
            except Exception as e:
                print('保存评论错误：', e.__str__())
            print('保存评论成功！')
            return result
        else:
            return None
