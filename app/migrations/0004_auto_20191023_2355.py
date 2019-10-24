# Generated by Django 2.2.6 on 2019-10-23 23:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0003_auto_20191023_2351'),
    ]

    operations = [
        migrations.AlterField(
            model_name='category',
            name='icon',
            field=models.CharField(blank=True, default='', max_length=100, null=True, verbose_name='分类图标'),
        ),
        migrations.AlterField(
            model_name='word',
            name='word',
            field=models.CharField(max_length=99, unique=True, verbose_name='单词及语句'),
        ),
        migrations.AlterField(
            model_name='word',
            name='word_tag',
            field=models.CharField(blank=True, default='', max_length=50, null=True, verbose_name='标签'),
        ),
    ]
