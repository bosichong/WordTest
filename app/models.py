from django.db import models
from django.contrib.auth.models import AbstractUser

class UserProfile(AbstractUser):
    '''
    用户表
    '''
    user_nick_name = models.CharField(max_length=24, verbose_name=u'用户昵称', default="")
    user_gender = models.CharField(max_length=10, choices=(("1","男"),("0","女")), default="1", verbose_name=u"性别选择")
    user_birday = models.DateField(verbose_name=u"用户生日", null=True, blank=True)
    user_detail = models.CharField(max_length=200, verbose_name=u"个人简介", default='')
    #需要安装 pip install Pillow
    user_image = models.ImageField(upload_to="image/user/%Y/%m", default="image/user/default.png", max_length=100, verbose_name=u"用户头像")

    class Meta:
        verbose_name=u'用户表'
        verbose_name_plural = verbose_name
    def __unicode__(self):
        return self.username


class Category(models.Model):
    """分类"""
    name = models.CharField(max_length=20, verbose_name='分类名称', default='')
    detail = models.CharField(max_length=100, verbose_name='分类介绍', default='')
    icon = models.CharField(max_length=100, verbose_name='分类图标', default='', null = True,blank = True,)
    sort_id = models.IntegerField(verbose_name='分类排序', default=1)

    class Meta:
        verbose_name = '分类'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name


class Word(models.Model):
    '''
    单词及语句表
    '''
    word = models.CharField(max_length=99, verbose_name='单词及语句',null = False, unique = True)
    ch_meaning = models.TextField(verbose_name='词语汉意', null = False,)
    word_tag=models.CharField(max_length=50, verbose_name='标签', default='',null = True,blank = True,)
    word_image = models.ImageField(upload_to="image/user/%Y/%m", default="image/default.png", max_length=100,
                                   verbose_name="单词配图")
    istype = models.CharField(max_length=10, choices=(("0","语句"),("1","单词")), default="1", verbose_name="类型选择")
    # 在django2.0后，定义外键和一对一关系的时候需要加on_delete选项，此参数为了避免两个表里的数据不一致问题，不然会报错：
    word_user = models.ForeignKey(UserProfile,on_delete=models.CASCADE, verbose_name=u'数据录入者', null=True, blank=True)
    word_create_time= models.DateTimeField(verbose_name='创建时间',  auto_now_add=True)
    word_update_time= models.DateTimeField(verbose_name='更新时间',  auto_now=True)
    categorys = models.ManyToManyField(Category)


    class Meta:
        verbose_name='单词表'
        verbose_name_plural = verbose_name
    def __unicode__(self):
        return self.word



class Questionbank(models.Model):
    '''
    题库表
    '''
    name = models.CharField(max_length=99, verbose_name='题库名称',null = False, unique = True)
    detail = models.CharField(max_length=100, verbose_name='题库介绍', default='')
    words = models.ManyToManyField(Word,verbose_name='题库内容')

    # 在django2.0后，定义外键和一对一关系的时候需要加on_delete选项，此参数为了避免两个表里的数据不一致问题，不然会报错：
    q_user = models.ForeignKey(UserProfile,on_delete=models.CASCADE, verbose_name='最后更新者', null=True, blank=True)
    q_create_time= models.DateTimeField(verbose_name='创建时间',  auto_now_add=True)
    q_update_time= models.DateTimeField(verbose_name='更新时间',  auto_now=True)


    class Meta:
        verbose_name='题库表'
        verbose_name_plural = verbose_name
    def __unicode__(self):
        return self.name


class Examination_results(models.Model):
    '''
    考试结果表
考试结果或分数 所考题库 考试使用时间 考试日期 考试者
    '''

    questionbank = models.ForeignKey(Questionbank,on_delete=models.CASCADE, verbose_name='考试题库', null=True, blank=True)
    score = models.IntegerField(verbose_name='考试得分', null=False)
    qbtime = models.IntegerField(verbose_name='考试所用时间（秒）', null=False)
    e_create_time = models.DateTimeField(verbose_name='考试时间', auto_now_add=True)
    e_user = models.ForeignKey(UserProfile, on_delete=models.CASCADE, verbose_name='考试者', null=True, blank=True)

    class Meta:
        verbose_name='考试结果'
        verbose_name_plural = verbose_name
    def __unicode__(self):
        return self.questionbank

class Answer_record(models.Model):
    '''
    答题记录表
    对或错 单词或语句ID  创建时间 考试者

    '''

    word =models.ForeignKey(Word,on_delete=models.CASCADE, verbose_name='所考单词', null=True, blank=True)
    isTrue = models.IntegerField(verbose_name='对错记录，0错1对', null=False)
    ar_create_time = models.DateTimeField(verbose_name='创建时间', auto_now_add=True)
    ar_user =models.ForeignKey(UserProfile, on_delete=models.CASCADE, verbose_name='考试者', null=True, blank=True)


    class Meta:
        verbose_name='答题记录'
        verbose_name_plural = verbose_name
    def __unicode__(self):
        return self.word



