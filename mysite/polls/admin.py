# -*- coding: utf-8 -*-
from django.contrib import admin

# Register your models here.
from .models import Question,Choice
class ChoiceInline(admin.TabularInline):
    model = Choice
    extra = 3
# 表示：Choice对象在Question的管理界面中编辑。默认提供足够3个Choice的空间。

# 注册Question模型
class QuestionAdmin(admin.ModelAdmin):
#http://python.usyiyi.cn/translate/django_182/intro/tutorial02.html
    fieldsets = [
        ('Question list',{'fields':['question_text']}),
        ('Date information',{'fields':['pub_date'],'classes':['collapse']})
    ]
    inlines = [ChoiceInline]
    list_display = ('question_text','pub_date','was_published_recently')
    list_filter = ['pub_date']
    search_fields = ['question_text']
admin.site.register(Question,QuestionAdmin)

# list_display 方法属性：http://python.usyiyi.cn/translate/django_182/ref/contrib/admin/index.html#django.contrib.admin.ModelAdmin.list_display