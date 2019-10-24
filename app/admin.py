# coding=utf-8
from django.contrib import admin
from django.utils.safestring import mark_safe

from .models import UserProfile,Word,Category,Questionbank,Examination_results,Answer_record


class UserProfileAdmin(admin.ModelAdmin):
    """用来显示用户相关"""
    # 用来显示用户字段
    list_display = ('username', 'user_nick_name', 'email', 'user_gender' )
    # 过滤器设置
    list_filter = ('username', 'user_nick_name', 'email')
    # 搜索
    search_fields = ('username', 'user_nick_name', 'email')


class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name','detail','sort_id')
    #过滤器设置
    list_filter = ('name','sort_id')

class WordAdmin(admin.ModelAdmin):
    list_display = ('word','ch_meaning',)
    #过滤器设置
    list_filter = ('word',)


class QuestionbankAdmin(admin.ModelAdmin):
    list_display = ('name','detail',)
    #过滤器设置
    list_filter = ('name',)


class Examination_resultsAdmin(admin.ModelAdmin):
    list_display = ('questionbank','score','score','qbtime','e_create_time','e_user',)
    #过滤器设置
    list_filter = ('questionbank','e_user')



class Answer_recordAdmin(admin.ModelAdmin):
    list_display = ('word','isTrue',)
    #过滤器设置
    list_filter = ('word','isTrue')

admin.site.register(UserProfile, UserProfileAdmin)
admin.site.register(Category,CategoryAdmin)
admin.site.register(Word,WordAdmin)
admin.site.register(Questionbank,QuestionbankAdmin)
admin.site.register(Answer_record,Answer_recordAdmin)
admin.site.register(Examination_results,Examination_resultsAdmin)