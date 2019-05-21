#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# 分词
import time

window_size = 4
def fmm(source, words_dict):
    len_source = len(source)  # 原句长度
    index = 0
    words = []  # 分词后句子每个词的列表

    while index < len_source:  # 如果下标未超过句子长度
        match = False
        for i in range(window_size, 0, -1):
            sub_str = source[index: index+i]
            if sub_str in words_dict:
                match = True
                words.append(sub_str)
                index += i
                break
        if not match:
            words.append(source[index])
            index += 1
    return words

def bmm(source, word_dict):
    len_source = len(source)  # 原句长度
    index = len_source
    words = []  # 分词后句子每个词的列表

    while index > 0:
        match = False
        for i in range(window_size, 0, -1):
            sub_str = source[index-i: index]
            if sub_str in words_dict:
                match = True
                words.append(sub_str)
                index -= i
                break
        if not match:
            words.append(source[index-1])
            index -= 1
    words.reverse()  # 得到的列表倒序
    return words

def bi_mm(source, word_dict):
    forward = fmm(source, words_dict)
    backward = bmm(source, words_dict)
    # 正反向分词结果
    print("FMM: ", forward)
    print("BMM: ", backward)
    # 单字词个数
    f_single_word = 0
    b_single_word = 0
    # 总词数
    tot_fmm = len(forward)
    tot_bmm = len(backward)
    # 非字典词数
    oov_fmm = 0
    oov_bmm = 0
    # 罚分，罚分值越低越好
    score_fmm = 0
    score_bmm = 0
    # 如果正向和反向结果一样，返回任意一个
    if forward == backward:
        return backward
    # print(backward)
    else:  # 分词结果不同，返回单字数、非字典词、总词数少的那一个
        for each in forward:
            if len(each) == 1:
                f_single_word += 1
        for each in backward:
            if len(each) == 1:
                b_single_word += 1
        for each in forward:
            if each not in words_dict:
                oov_fmm += 1
        for each in backward:
            if each not in backward:
                oov_bmm += 1
        # 可以根据实际情况调整惩罚分值
        # 这里都罚分都为1分
        # 非字典词越少越好
        if oov_fmm > oov_bmm:
            score_bmm += 1
        elif oov_fmm < oov_bmm:
            score_fmm += 1
        # 总词数越少越好
        if tot_fmm > tot_bmm:
            score_bmm += 1
        elif tot_fmm < tot_bmm:
            score_fmm += 1
        # 单字词越少越好
        if f_single_word > b_single_word:
            score_bmm += 1
        elif f_single_word < b_single_word:
            score_fmm += 1

        # 返回罚分少的那个
        if score_fmm < score_bmm:
            return forward
        else:
            return backward

def read_dict(path):
    words_dict = []
    with open(path, 'r', encoding='utf8') as r:
        line = r.readlines()
        # print(line)
        for i in line:
            word = i.split(' ')
            words_dict.append(word[0])
    return words_dict

if __name__ == '__main__':
    start = time.time()
    words_dict = read_dict('dict.txt')
    # print(bmm("我正在上自然语言处理课。", words_dict))
    # print("result: ", result)
    print("BiMM: ", bi_mm("家里第一次买这么大的电视，一次很带感的开箱，看我的评论请与我的配图一并服用。第一感觉，哇很大，打开包装，哇好长，把它小心翼翼搁在电视柜上，两个字完美，跟我家背景墙太搭了。不多说开机，色彩还是很棒的！不愧是ips屏它妈。现在还没接电视源，很期待带与小米盒子一起搭配使用。", words_dict))
    end = time.time()
    print("running time: " + str(end - start) + "s")
