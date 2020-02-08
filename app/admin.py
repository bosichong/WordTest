# coding=utf-8
from django.contrib import admin
from django.utils.safestring import mark_safe
from django.contrib.auth.admin import UserAdmin

from .models import UserProfile, Word, Category, Questionbank, Examination_results, Answer_record


# 通过继承UserAdmin来解决扩展用户后修改密码明文问题
class UserProfileAdmin(UserAdmin):
    """用来显示用户相关"""
    # 用来显示用户字段
    list_display = ('username', 'user_nick_name', 'email', 'user_gender')

    fieldsets = (
        (None, {'fields': ('username', 'password', 'first_name', 'last_name', 'email')}),
        (('User Information'),
         {'fields': ('user_nick_name', 'user_gender', 'user_birday', 'user_detail', 'user_image')}),
        (('Permissions'), {'fields': ('is_superuser', 'is_staff', 'is_active',
                                      'groups', 'user_permissions')}),
        (('Important dates'), {'fields': ('last_login', 'date_joined')}),

    )

    # 过滤器设置
    list_filter = ('username', 'user_nick_name', 'email')
    # 搜索
    search_fields = ('username', 'user_nick_name', 'email')


class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'detail', 'sort_id')
    # 过滤器设置
    list_filter = ('name', 'sort_id')


class WordAdmin(admin.ModelAdmin):
    # def has_change_permission(self, request, obj=None):
    #     has_class_permission = super(WordAdmin, self).has_change_permission(request, obj)
    #     if not has_class_permission:
    #         return False
    #     if obj is not None and not request.user.is_superuser and request.user.id != obj.word_user.id:
    #         return False
    #     return True
    #
    # def queryset(self, request):
    #     if request.user.is_superuser:
    #         return Word.objects.all()
    #     return Word.objects.filter(word_user=request.user)

    # def save_model(self, request, obj, form, change):
    #     if not change:
    #         obj.word_user = request.user
    #         super().save_model(request, obj, form, change)

    list_display = ('word', 'ch_meaning', 'word_user', 'word_tag',)
    filter_horizontal = ('categorys',)
    # ordering设置默认排序字段，负号表示降序排序
    ordering = ('-word_create_time',)
    radio_fields = {"istype": admin.VERTICAL}

    # 筛选器
    list_filter = ('categorys',)  # 过滤器
    search_fields = ('word',)  # 搜索字段
    date_hierarchy = 'word_create_time'  # 详细时间分层筛选　


class QuestionbankAdmin(admin.ModelAdmin):
    exclude = ('q_user',)  # 隐藏字段，自动填充

    # 显示自己添加的内容
    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs
        return qs.filter(q_user=request.user)

    # 隐藏字段，自动填充
    def save_model(self, request, obj, form, change):
        obj.q_user = request.user
        super().save_model(request, obj, form, change)

    list_display = ('name', 'detail', 'isopen', 'q_user')
    # 过滤器设置
    list_filter = ('name',)
    filter_horizontal = ('words',)

    date_hierarchy = 'q_create_time'  # 详细时间分层筛选　


class Examination_resultsAdmin(admin.ModelAdmin):
    list_display = ('questionbank', 'score', 'score', 'qbtime', 'e_create_time', 'e_user',)
    # 过滤器设置
    list_filter = ('questionbank', 'e_user')


class Answer_recordAdmin(admin.ModelAdmin):
    list_display = ('word', 'isTrue',)
    # 过滤器设置
    list_filter = ('word', 'isTrue')


admin.site.site_header = 'WordTest 后台管理'
admin.site.site_title = 'WordTest 后台管理'

admin.site.register(UserProfile, UserProfileAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Word, WordAdmin)
admin.site.register(Questionbank, QuestionbankAdmin)
admin.site.register(Answer_record, Answer_recordAdmin)
admin.site.register(Examination_results, Examination_resultsAdmin)
