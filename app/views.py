# coding=utf-8

#启动虚拟环境
# source /Users/mac/pywork/django226/bin/activate

from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required

from django.http import HttpResponse

from .models import *
from .utils import *

import time
import random


@login_required
def index(request):
    user = request.user
    ms = Questionbank.objects.filter(q_user=user,).order_by('-q_create_time')
    myqbs = []
    for m in ms:
        c = Examination_results.objects.filter(questionbank=m, e_user=user).count()
        # 题库信息：名称 简介 使用次数 题库ID 题库中的题数
        myqbs.append([m.name, m.detail, c, m.id,m.words.all().count()])

    oms = Questionbank.objects.filter(isopen='1').order_by('-q_create_time')
    opqbs = []
    for m in oms:
        c = Examination_results.objects.filter(questionbank=m, e_user=user).count()
        # 题库信息：名称 简介 使用次数 题库ID 题库中的题数
        opqbs.append([m.name, m.detail, c, m.id,m.words.all().count()])


    return render(request, 'app/index.html', {'myqbs': myqbs,
                                              'opqbs':opqbs
                                              })

@login_required
def qindex(request):
    '''答题首页'''
    qbid = int(request.GET.get('qbid', '0'))  # 默认为第一题
    # 取出题库相关信息  后期PK换成题库的ID
    qb = Questionbank.objects.get(pk=qbid)
    qblist = []  # 题库list
    for w in qb.words.all():
        qblist.append([w.word, w.ch_meaning, w.id])
    tit = qb.name
    detail = qb.detail
    c = qb.words.all().count()
    random.shuffle(qblist)  # 随机打乱
    ###session中需要存储的选项。
    request.session['qb'] = qblist  # 本次考试所有题
    request.session['qbid'] = qb.id  # 题库ID
    request.session['answers'] = []  # 答案列表
    request.session['start'] = True  # 本次答题开始
    request.session['p'] = 0  # 本次答题开始
    request.session['starttime'] = time.time()

    p = 0

    return render(request, 'app/qindex.html', {
        'tit': tit,
        'detail': detail,
        'p': p,
        'c':c,
    })

@login_required
def q(request):
    '''答题页'''

    p = request.session.get('p')  # 默认为第一题

    answer = request.GET.get('answer', '')  # 答案
    # 记录答案
    answers = request.session.get('answers')
    if p > 0:
        answers.append(answer)

    request.session['answers'] = answers

    s = request.session.get('qb')[p]
    isend = 'q'
    btn = '下一题'
    # 答题结束后跳的结束页面
    if p >= len(request.session['qb']) - 1:
        isend = 'qend'
        btn = '结束答题'

    request.session['p'] = request.session.get('p') + 1
    print ('p:',request.session.get('p'))

    progress = (request.session.get('p')/len(request.session.get('qb')))*100
    print (request.session.get('p')/len(request.session.get('qb')),progress)

    return render(request, 'app/q.html', {
        's': s,
        'isend': isend,
        'btn': btn,
        'progress':progress,
    })

@login_required
def qend(request):
    '''答题结束页面'''
    # 接收最一题的答案
    answer = request.GET.get('answer', '0')  # 答案
    if request.session.get('start'):
        answers = request.session.get('answers')
        answers.append(answer)
        request.session['answers'] = answers

    #####################
    qb = Questionbank.objects.get(pk=request.session['qbid'])

    tit = qb.name
    detail = qb.detail
    qresult = []  # 包含题，正确答案及用户的答案

    qberr = 0  # 错误题数
    for i, j in zip(request.session.get('qb'), request.session.get('answers')):
        ico = 'btn btn-success', 'glyphicon glyphicon-ok'
        cls = ''
        if j != i[0]:
            qberr += 1
            ico = 'btn btn-danger', 'glyphicon glyphicon-remove'
            cls = 'warning'
        qresult.append([i[1], i[0], j, ico, cls, i[2]])
    score = rtscore(qberr, len(request.session.get('qb')))#得分

    # print ("本次考试得分:",score)
    ###数据入库操作
    # 考试结果入库
    # er = Examination_results()

    if request.session.get('start'):
        print ("数据入库准备！只有一次机会，防止重复添加数据！")

        dtime = rtdtime(request.session.get('starttime'), time.time())
        # print (round(dtime))

        er = Examination_results()  # 本次考试结果
        er.questionbank = qb
        er.score = score
        er.qbtime = dtime
        er.e_user = request.user
        er.save()  # 存储本次考试结果

        for rs in qresult:
            ar = Answer_record()
            w = Word.objects.get(pk=rs[5])
            ar.word = w
            ar.answer = rs[2]
            if rs[2] == w.word:
                ar.isTrue = 1
            else:
                ar.isTrue = 0
            ar.er = er

            ar.ar_user = request.user

            ar.save()

    # 答题结束，防止再次提交数据入库
    request.session['start'] = False
    return render(request, 'app/qend.html', {
        'tit': tit,
        'detail': detail,
        'qresult': qresult,
        'score': score,
    })





def score(request):
    '''考试结果分析页面'''

    es = Examination_results.objects.filter(e_user=request.user).order_by('-e_create_time')[:8]
    ers = []
    for e in es:

        ers.append((e.questionbank.name,e.score,rttime(e.qbtime),e.e_create_time))


    ans = Answer_record.objects.filter(ar_user=request.user,isTrue=0)
    ars = []

    for a in ans:
        ars.append((a.word.word,a.answer,a.er.questionbank.name))

    errs = rtars(ars)[:8]
    ers1 = []

    for e in errs:
        w = Word.objects.filter(word=e)
        # print (w)
        k = Answer_record.objects.filter(ar_user=request.user, isTrue=0, word=w[:1]).count()
        ers1.append((e,k))



    return  render(request,'app/score.html',{'ers':ers,
                                             'ars':ars,
                                             'ers1':ers1
                                             })




def sitelogin(request):
    error_msg = ' '
    if request.method == "GET":
        return render(request, "app/login.html")
    if request.method == "POST":
        username = request.POST.get("username")
        print(username)
        password = request.POST.get("password")
        print(password)
        user = authenticate(username=username, password=password)  # 只是验证功能，还没有登录

        if user:
            print(user)  # username
            print(type(user))  # <class 'django.contrib.auth.models.User'>
            login(request, user)  # 验证通过，登录
            # 内部有request.user=user     可以用模板{{request.user}}
            return redirect(request.GET.get("next", '/app'))  # 登陆后跳转到首页
            # 登录成功默认跳转用户信息页面，如果是其他页面来的，登录后跳转到其他页面
        else:
            print('user')  # None
            print(type(user))  # <class 'NoneType'>
            error_msg = "用户名或密码错误"
        return render(request, "app/login.html", {"error_msg": error_msg})


def sitelogout(request):
    logout(request)
    return redirect('/app')







def cj(request):
    words = rtwords()#获取采集的单词数据

    user = UserProfile.objects.get(pk=1)#数据采集者
    c = Category.objects.get(pk=54)#取其他分类 把采集单词装到这个分类里
    # 校验结果入库
    con = 0
    ns = []
    for ws in words:
        # 组装分类并入库
        # c = Category()
        # c.name = ws[0]
        # c.detail = ws[0]
        # c.sort_id = 99
        # c.c_user = user
        # c.save()
        # print(c,'分类添加成功！')
        for w in ws[1]:
            # 组装单词 并入库

            if not Word.objects.filter(word=w[0]):
                word = Word()
                word.word = w[0]
                word.ch_meaning = w[1]
                word.istype = 1
                word.word_user = user
                word.save()
                # 多对多添加分类

                word.categorys.add(c)
                print(word,'单词添加成功')
                con+=1
            else:
                ns.append(w[0])
    print (ns)
    print ('添加成功：',con,'个单词')

    return render(request, "app/cj.html", {"words": words,
                                           'user':user,})