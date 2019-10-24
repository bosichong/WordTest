# coding=utf-8
from django.shortcuts import render

from django.http import HttpResponse


def index(request):
    msg = '首页test测试'
    return render(request, 'index.html', {'msg': msg,
                                              })

