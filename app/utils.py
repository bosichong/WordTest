# coding=utf-8

from bs4 import BeautifulSoup
import requests





def rtars(ls):
    '''
    python按重复数字的次数降序排列返回数组

数组结构范例，以索引0为基准进行排序。

[('line', 'this', '程序测试题库(2)(私有题库)'),
('front', 'fornt', '程序测试题库(2)(私有题库)'),
('first', 'start', '程序测试题库(2)(私有题库)'),
('last', 'end', '程序测试题库(2)(私有题库)'),
('level', 'shui', '程序测试题库(2)(私有题库)'),
('right', 'hao', '程序测试题库(1)(公开题库)'),
('boss', 'boos', 'Test的私有题库（一）'),
('part', 'ss', 'Test的私有题库（一）'),
('boss', 's', 'Test的私有题库（一）'),
('need', 's', 'Test的私有题库（一）'),
('sound', 'd', 'Test的私有题库（一）'),
('word', 's', 'Test的私有题库（一）'),
('title', 'ti', 'Test的私有题库（一）')]

    :param l:
    :return:
    '''
    a =[]
    for i in ls:
        a.append(i[0])

    # 取出数字出现的次数放进L中,并降序排序
    L = []
    for i in a:
        L.append(a.count(i))
    L = list(set(L))
    L.sort(reverse=True)

    # 取出次数对应a列表里面的值放进新列表num1中
    num1 = []
    for m in L:
        for n in a:
            if m == a.count(n):
                num1.append(n)

    # 去重
    num2 = []
    for i in num1:
        if i not in num2:
            num2.append(i)

    return num2

def rttime(s):
    """返回时间分钟"""
    if not s//60:
        return '{:.0f}秒'.format( s % 60)
    else:
        return '{:.0f}分,{:.0f}秒'.format(s // 60, s % 60)

def rtscore(err, lenqbs):
    '''
    返回考试得分
    :param err: 错题数
    :param lenqbs: 考题总数
    :return: int
    '''
    return round((1 - err / lenqbs) * 100)


def rtdtime(s, e):
    '''
    返回所用时间秒
    :param s:
    :param e:
    :return: int
    '''
    return e - s

def rtwords():

    '''
    采集小学生英文单词入库
    采集地址：
    http://127.0.0.1:8000/static/words/words.html
    此库采集单词 593

    http://127.0.0.1:8000/static/words/w.html
    此库采集单词 977
    也是最终使用的单词数据


    '''

    # 获取html代码
    r = requests.get('http://127.0.0.1:8000/static/words/words.html')
    r.encoding = 'utf-8'  # 设置编码
    soup = BeautifulSoup(r.text, 'html.parser')
    # print(soup.prettify())

    ps = soup.find_all(attrs={'class': 'title'})
    tabs = soup.find_all('table')
    words = []  # 所有单词
    # list结构预览
    # [['名称',[['apple','pen],['苹果','铅笔'],]]，['名称',[['apple','pen],['苹果','铅笔'],]]]

    for c, t in zip(ps, tabs):

        tmp = c.text.split("、", 1)
        title = tmp[1]
        ws = []  # 一组分类标题+所在单词
        ws.append(title)

        trs = t.find_all('tr')
        tws = []  # 整个分类下的所有单词
        for tr in trs:
            tds = tr.find_all('span')
            w = []  # 每个单词的拼装，例：['pen','铅笔']
            for td in tds:
                w.append(td.text)

            tws.append(w)
        ws.append(tws)
        words.append(ws)





    # # 获取html代码
    # r = requests.get('http://127.0.0.1:8000/static/words/w.html')
    # r.encoding = 'utf-8'  # 设置编码
    # soup = BeautifulSoup(r.text, 'html.parser')
    # # print(soup.prettify())
    #
    # ps = soup.find_all('p')
    # tabs = soup.find_all('table')
    # words = []  # 所有单词
    # # list结构预览
    # # [['名称',[['apple','pen],['苹果','铅笔'],]]，['名称',[['apple','pen],['苹果','铅笔'],]]]
    #
    # for c, t in zip(ps, tabs):
    #
    #     title = c.text
    #     ws = []  # 一组分类标题+所在单词
    #     ws.append(title)
    #
    #     trs = t.find_all('tr')
    #     tws = []  # 整个分类下的所有单词
    #     for tr in trs:
    #         tds = tr.find_all('td')
    #         w = []  # 每个单词的拼装，例：['pen','铅笔']
    #         for td in tds:
    #             w.append(td.text)
    #
    #         tws.append(w)
    #     ws.append(tws)
    #     words.append(ws)











    return words
