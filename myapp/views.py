from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.views.decorators.csrf import csrf_exempt
from .spidercore.SpiderUtil import Spiders
from urllib.parse import quote
from .nlpcore.NLPHelper import NLPHelper
from .models import Base, Comments, Analysis, Sorts
from django.db.models import Q, Avg
import matplotlib.pyplot as plt

# Create your views here.

plt.switch_backend('agg')
plt.rcParams['font.sans-serif'] = ['SimHei']  # 正常显示中文标签
plt.rcParams['axes.unicode_minus'] = False  # 正常显示负号
spider = Spiders()
url_templates = {'item.jd.com': '京东商城',
                 'product.suning.com': '苏宁易购',
                 'detail.tmall.com': '天猫商城',
                 'detail.vip.com': '唯品会'}


def visual():
    jd_base_model = Base.objects.filter(platform_id=1)
    sn_base_model = Base.objects.filter(platform_id=3)
    vip_base_model = Base.objects.filter(platform_id=4)

    platform_avg_path = 'static/charts/platform_avg.png'
    jd_avg_path = 'static/charts/jd_avg.png'
    sn_avg_path = 'static/charts/sn_avg.png'
    vip_avg_path = 'static/charts/vip_avg.png'

    sorts_model = Sorts.objects.all()
    sorts_list = []
    for item in sorts_model:
        sorts_list.append(item.__dict__)
    # print('所有种类：', sorts_list)
    jd_avg_score = 0
    sn_avg_score = 0
    vip_avg_score = 0

    jd_sorts_avg = {}
    sn_sorts_avg = {}
    vip_sorts_avg = {}
    # 计算平台各种类的均值
    for item in sorts_list:
        k = item.get('id')
        v = item.get('sorts_name')
        for item in jd_base_model:
            model_url = item.__dict__.get('product_url')
            sorts_id = item.__dict__.get('sorts_id')
            if k == sorts_id:
                sorts_score = Comments.objects.filter(product_url=model_url).aggregate(Avg('sent_score')).get(
                    'sent_score__avg')
                if jd_sorts_avg.get(v) is not None:
                    jd_sorts_avg[v] = round((float(jd_sorts_avg[v]) + float(sorts_score)) / 2, 4)
                else:
                    jd_sorts_avg[v] = round(float(sorts_score), 4)
        for item in sn_base_model:
            model_url = item.__dict__.get('product_url')
            sorts_id = item.__dict__.get('sorts_id')
            if k == sorts_id:
                sorts_score = Comments.objects.filter(product_url=model_url).aggregate(Avg('sent_score')).get(
                    'sent_score__avg')
                if sn_sorts_avg.get(v) is not None:
                    sn_sorts_avg[v] = round((float(sn_sorts_avg[v]) + float(sorts_score)) / 2, 4)
                else:
                    sn_sorts_avg[v] = round(float(sorts_score), 4)
        for item in vip_base_model:
            model_url = item.__dict__.get('product_url')
            sorts_id = item.__dict__.get('sorts_id')
            if k == sorts_id:
                sorts_score = Comments.objects.filter(product_url=model_url).aggregate(Avg('sent_score')).get(
                    'sent_score__avg')
                if vip_sorts_avg.get(v) is not None:
                    vip_sorts_avg[v] = round((float(vip_sorts_avg[v]) + float(sorts_score)) / 2, 4)
                else:
                    vip_sorts_avg[v] = round(float(sorts_score), 4)

    # 计算各平台的平均分
    for item in jd_base_model:
        model_url = item.__dict__.get('product_url')
        sorts_id = item.__dict__.get('sorts_id')
        j_score = Comments.objects.filter(product_url=model_url).aggregate(Avg('sent_score'))
        jd_avg_score += float(j_score.get('sent_score__avg'))
    jd_avg_score = round(jd_avg_score / len(jd_base_model), 4)

    for item in sn_base_model:
        model_url = item.__dict__.get('product_url')
        s_score = Comments.objects.filter(product_url=model_url).aggregate(Avg('sent_score'))
        sn_avg_score += float(s_score.get('sent_score__avg'))
    sn_avg_score = round(sn_avg_score / len(sn_base_model), 4)

    for item in jd_base_model:
        model_url = item.__dict__.get('product_url')
        v_score = Comments.objects.filter(product_url=model_url).aggregate(Avg('sent_score'))
        vip_avg_score += float(v_score.get('sent_score__avg'))
    vip_avg_score = round(vip_avg_score / len(vip_base_model), 4)

    X = ['京东', '苏宁', '唯品会']
    Y = [jd_avg_score, sn_avg_score, vip_avg_score]
    plt.figure(figsize=(5, 5))
    plt.bar(X, Y, width=0.5, color='#87CEFA')
    plt.ylim(0, 2)
    plt.xlabel('平均情感得分')
    plt.ylabel('电商平台')
    plt.title('电商平台平均情感得分')
    plt.savefig(platform_avg_path)
    plt.close()

    X = []
    Y = []
    for k, v in jd_sorts_avg.items():
        X.append(k)
        Y.append(v)
    plt.figure(figsize=(5, 5))
    plt.bar(X, Y, width=0.5, color='#87CEFA')
    plt.ylim(0, 2)
    plt.xlabel('商品分类')
    plt.ylabel('平均得分')
    plt.title('京东-商品类别平均情感得分')
    plt.savefig(jd_avg_path)
    plt.close()

    X = []
    Y = []
    for k, v in sn_sorts_avg.items():
        X.append(k)
        Y.append(v)
    plt.figure(figsize=(5, 5))
    plt.bar(X, Y, width=0.5, color='#87CEFA')
    plt.ylim(0, 2)
    plt.xlabel('商品分类')
    plt.ylabel('平均得分')
    plt.title('苏宁-商品类别平均情感得分')
    plt.savefig(sn_avg_path)
    plt.close()

    X = []
    Y = []
    for k, v in vip_sorts_avg.items():
        X.append(k)
        Y.append(v)
    plt.figure(figsize=(5, 5))
    plt.bar(X, Y, width=0.5, color='#87CEFA')
    plt.ylim(0, 2)
    plt.xlabel('商品分类')
    plt.ylabel('平均得分')
    plt.title('唯品会-商品类别平均情感得分')
    plt.savefig(vip_avg_path)
    plt.close()

    # print('京东平均分：', jd_avg_score)
    # print('苏宁平均分：', sn_avg_score)
    # print('唯品会平均分:', vip_avg_score)
    # print('京东分类:', jd_sorts_avg)
    # print('苏宁分类:', sn_sorts_avg)
    # print('唯品会分类:', vip_sorts_avg)
    print('统计分析结果保存成功')
    return {'all_avg_path': '../'+platform_avg_path,
            'jd_avg_path': '../'+jd_avg_path,
            'sn_avg_path': '../'+sn_avg_path,
            'vip_avg_path': '../'+vip_avg_path}


def welcome(request):
    return render(request, 'myapp/index.html')


def analysis(request):
    req = request.GET.get('purl')
    count = request.GET.get('count')

    if count == '':
        count = 100
    page = int(count) // 10 + 1
    print('page:', page)
    print('待分析的商品链接:', req)
    print('待分析数量:', count)

    visual_dict = {}

    base_info_model = Base()
    com_info_model = Comments()
    anly_info_model = Analysis()

    # 推荐
    recommend_list = []

    comm_list = []
    com_model = None
    result = None

    if Base.objects.filter(product_url=req).first() is not None:
        print('存在原始记录:')
        com_model = Base.objects.filter(product_url=req).first().__dict__

        result = Analysis.objects.filter(product_url=req).first().__dict__

        recommend_model = Base.objects.filter(Q(platform_id=com_model.get('platform_id'))
                                              & ~Q(product_url=req)
                                              & Q(sorts_id=com_model.get('sorts_id')))
        # print(recommend_model)
        print('推荐：')
        for item in recommend_model:
            recommend_list.append(item.__dict__)
        comm_m = Comments.objects.filter(product_url=com_model.get('product_url'))
        for item in comm_m:
            comm_list.append(item.old_text)

    else:
        print('新的链接!正在分析...')
        nlp_helper = NLPHelper()
        com_model, comm_list = spider.start_comments(product_url=req, page=page)

        if com_model is not None and len(comm_list) > 0:

            result = nlp_helper.start(platform_id=com_model.get('platform_id'),
                                      product_url=com_model.get('product_url'),
                                      product_id=com_model.get('product_id'),
                                      comments_dict=nlp_helper.list2dict(comm_list))

            recommend_model = Base.objects.filter(Q(platform_id=com_model.get('platform_id'))
                                                  & ~Q(product_url=req)
                                                  & Q(sorts_id=com_model.get('sorts_id')))

            print('推荐：')
            for item in recommend_model:
                recommend_list.append(item.__dict__)

            print('正在保存商品基础信息...')
            base_info_model.product_title = com_model.get('product_title')
            base_info_model.product_id = com_model.get('product_id')
            base_info_model.product_url = com_model.get('product_url')
            base_info_model.platform_id = com_model.get('platform_id')
            base_info_model.good_num = com_model.get('good_num')
            base_info_model.mid_num = com_model.get('mid_num')
            base_info_model.poor_num = com_model.get('poor_num')
            base_info_model.total_num = com_model.get('total_num')
            base_info_model.sorts_id = com_model.get('sorts_id')
            base_info_model.img_url = com_model.get('img_url')
            base_info_model.good_rote = com_model.get('good_rote')
            base_info_model.save()
            print('保存基础信息成功!', com_model.get('product_url'))

            print('正在保存分析结果...')
            anly_info_model.product_url = req
            anly_info_model.product_id = com_model.get('product_id')
            anly_info_model.good_rote = result.get('good_rote')
            anly_info_model.poor_rote = result.get('poor_rote')
            anly_info_model.good_num = result.get('good_num')
            anly_info_model.mid_num = result.get('mid_num')
            anly_info_model.poor_num = result.get('poor_num')
            anly_info_model.total_num = result.get('total_num')
            anly_info_model.all_cloud = result.get('all_cloud')
            anly_info_model.good_cloud = result.get('good_cloud')
            anly_info_model.poor_cloud = result.get('poor_cloud')
            anly_info_model.all_sent_h = result.get('all_sent_h')
            anly_info_model.good_sent_h = result.get('good_sent_h')
            anly_info_model.poor_sent_h = result.get('poor_sent_h')
            anly_info_model.mid_sent_h = result.get('mid_sent_h')
            anly_info_model.top_all_freq = result.get('top_all_freq')
            anly_info_model.top_good_freq = result.get('top_good_freq')
            anly_info_model.top_poor_freq = result.get('top_poor_freq')
            anly_info_model.save()
            print('保存分析结果成功！')

        else:
            return render(request, 'myapp/index.html', {'msg': '警告:商品抓取失败！请检查评论数量或网络状况！'})
    visual_dict = visual()
    return render(request, 'myapp/result.html', {
        'spider_result': com_model,
        'result': result,
        'recommend': recommend_list,
        'comment': comm_list[0:7],
        'visual_result': visual_dict
    })


def search(request):
    req = request.POST.get('search_key')
    count = request.POST.get('count')
    if count is None:
        count = '100'
    is_goods_search = False
    is_comments_search = False
    is_not_support = False

    for k, v in url_templates.items():
        if req.startswith('http') or req.startswith('https'):
            if k in req:
                # 抓取评论并分析
                is_comments_search = True
                is_not_support = False
                break
                return render(request, 'myapp/result.html')
            else:
                is_not_support = True
                # break
        else:
            # 抓取商品列表
            is_goods_search = True
            break

    if is_comments_search:
        # 抓取并分析评论,则重定向到analysis
        return HttpResponseRedirect('../analysis?purl=' + req + '&count=' + count)
    elif is_goods_search:
        # 多平台商品搜索
        print('接收的搜索关键字:', req)
        result = spider.start_goods(keyword=req)
        jd_url = result.get('jd').get('url')
        # tm_url = result.get('tm').get('url')
        sn_url = result.get('sn').get('url')
        vip_url = result.get('vip').get('url')
        jd_list = result.get('jd').get('result')
        # tm_list = result.get('tm').get('result')
        sn_list = result.get('sn').get('result')
        vip_list = result.get('vip').get('result')
        return render(request, 'myapp/search.html', {
            'jd_url': jd_url,
            'jd_list': jd_list,
            # 'tm_url': tm_url,
            # 'tm_list': tm_list,
            'sn_url': sn_url,
            'sn_list': sn_list,
            'vip_url': vip_url,
            'vip_list': vip_list
        })
    elif is_not_support:
        print('未支持的链接！')
        return render(request, 'myapp/index.html', {'msg': '警告:未支持的链接!'})
