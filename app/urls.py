# coding=utf-8
from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('qindex', views.qindex, name='qindex'),
    path('q', views.q, name='q'),
    path('qend', views.qend, name='qend'),
    path('score', views.score, name='score'),

    path('login', views.sitelogin, name='login'),
    path('logout', views.sitelogout, name="logout"),

    path('cj', views.cj, name='cj'),
]
