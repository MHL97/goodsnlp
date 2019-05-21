#!/usr/bin/env python3
# -*- coding: utf-8 -*-


"""
商品评论信息的可视化
"""

import wordcloud
import matplotlib.pyplot as plt


plt.switch_backend('agg')
plt.rcParams['font.sans-serif'] = ['SimHei']  # 正常显示中文标签
plt.rcParams['axes.unicode_minus'] = False  # 正常显示负号


def dict2list(old_dict):
    new_list = []
    for k, v in old_dict.items():
        new_list.append(v)
    return new_list


def get_word_cloud(platform_id, product_id, word_list, word_type):
    if len(word_list) < 1:
        return ''
    save_root = 'static/'
    save_url = 'wordclouds/' + platform_id + '-'+product_id + '_{}_wordcloud.png'.format(word_type)
    word_str = "".join(word_list)
    wordc = wordcloud.WordCloud(font_path='simfang.ttf')
    wordc.generate(word_str)
    plt.imshow(wordc)
    plt.axis("off")
    wordc.to_file(save_root + save_url)
    plt.close()
    print('WordCloud img of ', word_type, 'make successfully!')
    return save_root + save_url


def start_analysis(platform_id, product_id, score_dict, all_sentence_dict, tf_idf_dict):

    # 结果集
    result = {}
    result['total_num'] = len(score_dict)
    save_root = 'static/'
    save_url = save_root + 'charts/' + platform_id + '-'+product_id + '_{}_sentiment_hist.png'
    save_url_freq = save_root + 'charts/' + platform_id + '-'+product_id + '_{}_freq.png'
    # 分数集
    good_score_list = []
    mid_score_list = []
    poor_score_list = []
    all_score_list = []

    # 评论情感定位集
    good_sentence_list = []
    poor_sentence_list = []
    # 评论关键字集
    mid_comm_list = []
    poor_comm_list = []
    good_comm_list = []
    # 关键字词频集
    good_freq = {}
    poor_freq = {}
    all_freq = {}
    good_count = 0
    mid_count = 0
    poor_count = 0

    sent_sort_dict = {}
    # 分类聚合
    for k, v in score_dict.items():
        all_score_list.append(v)
        if 0 < v and v < 0.1:
            # print('差评：', all_sentence_dict.get(k))
            poor_count += 1
            sent_sort_dict[k] = '0'
            poor_sentence_list.append(all_sentence_dict.get(k))
            poor_score_list.append(v)
            poor_comm_list.append(tf_idf_dict.get(k))
        elif v >= 0.1 and v <= 0.5:
            sent_sort_dict[k] = '1'
            mid_count += 1
            mid_score_list.append(v)
            good_sentence_list.append(all_sentence_dict.get(k))
            mid_comm_list.append(tf_idf_dict.get(k))
        elif v > 0.5:
            sent_sort_dict[k] = '1'
            good_count += 1
            good_score_list.append(v)
            good_sentence_list.append(all_sentence_dict.get(k))
            good_comm_list.append(tf_idf_dict.get(k))
    # 词云
    result['all_cloud'] = '../' + get_word_cloud(platform_id=platform_id,
                                                     product_id=product_id,
                                                     word_list=dict2list(all_sentence_dict),
                                                     word_type='all')
    result['good_cloud'] = '../' + get_word_cloud(platform_id=platform_id,
                                                      product_id=product_id,
                                                      word_list=good_sentence_list,
                                                      word_type='good')
    result['poor_cloud'] = '../' + get_word_cloud(platform_id=platform_id,
                                                      product_id=product_id,
                                                      word_list=poor_sentence_list,
                                                      word_type='poor')
    # 统计好评、差评、总词频
    for k, v in tf_idf_dict.items():
        for word in v:
            if all_freq.get(word):
                all_freq[word] += 1
            else:
                all_freq[word] = 1
    for item in poor_comm_list:
        for word in item:
            if poor_freq.get(word):
                poor_freq[word] += 1
            else:
                poor_freq[word] = 1
    for item in mid_comm_list:
        # 中评词频也算在好评中
        for word in item:
            if good_freq.get(word):
                good_freq[word] += 1
            else:
                good_freq[word] = 1
    for item in good_comm_list:
        for word in item:
            if good_freq.get(word):
                good_freq[word] += 1
            else:
                good_freq[word] = 1
    # 取top10
    top_good = sorted(good_freq.items(), key=lambda item: item[1], reverse=True)[0:10]
    top_poor = sorted(poor_freq.items(), key=lambda item: item[1], reverse=True)[0:10]
    top_all = sorted(all_freq.items(), key=lambda item: item[1], reverse=True)[0:10]
    # 作词频统计图
    X = []
    Y = []
    for item in top_all:
        X.append(item[0])
        Y.append(item[1])
    plt.figure(figsize=(5, 5))
    plt.bar(X, Y)
    plt.xlabel('好评关键字')
    plt.ylabel('次数')
    plt.title('前十关键字统计(总)')
    plt.savefig(save_url_freq.format('top10all'))
    plt.close()
    result['top_all_freq'] = '../' + save_url_freq.format('top10all')
    print('Top 10 all save successfully!')

    X = []
    Y = []
    for item in top_good:
        X.append(item[0])
        Y.append(item[1])
    plt.figure(figsize=(5, 5))
    plt.bar(X, Y)
    plt.xlabel('好评关键字')
    plt.ylabel('次数')
    plt.title('前十关键字统计(好评)')
    plt.savefig(save_url_freq.format('top10good'))
    plt.close()
    result['top_good_freq'] = '../' + save_url_freq.format('top10good')
    print('Top 10 good save successfully!')

    X = []
    Y = []
    for item in top_poor:
        X.append(item[0])
        Y.append(item[1])
    plt.figure(figsize=(5, 5))
    plt.bar(X, Y)
    plt.xlabel('差评关键字')
    plt.ylabel('次数')
    plt.title('前十关键字统计(差评)')
    plt.savefig(save_url_freq.format('top10poor'))
    plt.close()
    result['top_poor_freq'] = '../' + save_url_freq.format('top10poor')
    print('Top 10 poor save successfully!')
    # 计算好评率和差评率
    try:
        good_rote = round((good_count) / len(score_dict), 2) * 100
        poor_rote = round(poor_count / len(score_dict), 2) * 100
    except Exception as e:
        print('计算错误，评论集数量为0.')
        return None, None

    result['good_num'] = good_count
    result['mid_num'] = mid_count
    result['poor_num'] = poor_count
    result['good_rote'] = good_rote
    result['poor_rote'] = poor_rote

    # 作分数集的直方图
    plt.xlabel('情感得分')
    plt.ylabel('数量')
    plt.title('情感得分(总)')
    plt.hist(all_score_list, bins=5)
    plt.savefig(save_url.format('all'))
    plt.close()
    result['all_sent_h'] = '../' + save_url.format('all')
    print('All_Hist save successfully!')

    plt.title('情感得分(好评)')
    plt.hist(good_score_list, bins=5)
    plt.savefig(save_url.format('good'))
    plt.close()
    result['good_sent_h'] = '../' + save_url.format('good')
    print('Good_Hist save successfully!')

    plt.title('情感得分(中评)')
    plt.hist(mid_score_list, bins=5)
    plt.savefig(save_url.format('mid'))
    plt.close()
    result['mid_sent_h'] = '../' + save_url.format('mid')
    print('Mid_Hist save successfully!')

    plt.title('情感得分(差评)')
    plt.hist(poor_score_list, bins=5)
    plt.savefig(save_url.format('poor'))
    plt.close()
    result['poor_sent_h'] = '../' + save_url.format('poor')
    print('Poor_Hist save successfully!')

    return result, sent_sort_dict


if __name__ == '__main__':
    pass
