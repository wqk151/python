# -*- coding: utf-8 -*-
from django.db import models
import datetime
from django.utils import timezone
# Create your models here.
class Question(models.Model):
    # 每个Field实例的名字(例如question_text或pub_date)就是字段的名字，数据库中作为表的列名。
    # Field的第一个参数（例如'date published'）来制定一个人类可读的名字，可以兼作文档，这是可选的。
    # 某些Field类具有必选参数。例如CharField要求你给它一个max_length。这个参数用于数据库模式，也可以用于数据验证。
    question_text = models.CharField(max_length=200)
    pub_date = models.DateTimeField('date published')
    def __str__(self):
        return self.question_text
    def was_published_recently(self):
        now = timezone.now()
        return now - datetime.timedelta(days=1) <= self.pub_date <= now
       # return self.pub_date >= timezone.now() - datetime.timedelta(days=1)
    was_published_recently.admin_order_field = 'pub_date'
    was_published_recently.boolean = True
    was_published_recently.short_description = 'Published recently?'
class Choice(models.Model):
    question = models.ForeignKey(Question)  # 一对多(自己是多)，一个问题可以有许多投票,ForeignKey--属于，这个投票属于某个问题
    choice_text = models.CharField(max_length=200)
    votes = models.IntegerField(default=0)
    def __str__(self):
        return self.choice_text
'''
python manage.py makemigrations polls
通过运行makemigrations告诉Django，已经对模型做了一些修改（本例是创建了新的模型），并且会将这些更改存储为迁移文件。
迁移是Django如何存储模型的变化，它们只是磁盘上的文件。这个文件就是polls/migrations/0001_initial.py。
sqlmigrate命令接收迁移文件的名字并返回它们的SQL语句：
python manage.py sqlmigrate polls 0001
注意：
1、输出的具体内容会会依据使用数据库而不同。
2、表名是自动生成，由APP的名字（polls）和模型名字的小写字母组合而成--question和choice。
3、主键（IDs）是自动添加的。
4、按照惯例，Django会在外键的字段名后面添加"_id"
5、外键关系由FOREIGN KEY约束式声明。
6、这些SQL语句是针对你所使用的数据库定制的，所以会包含某些数据库特有字段。
7、sqlmigrate命令并不会在你的数据库上真正运行迁移文件--它只是把Django任务需要的SQL打印在屏幕上。
8、可以运行python manage.py check 检查项目中的模型是否存在问题，而不用执行迁移或者接触数据库。

运行migrate以在你数据库中创建模型所对应的表：
python manage.py migrate
模型改变的三个步骤：
1、修改模型（models.py）
2、运行python manage.py makemigrations 为这些修改创建迁移文件
3、运行python manage.py migrate 将这些改变更新到数据库中。
'''
'''
Django提供的查询API
python manage.py shell

>>> from polls.models import Question, Choice
>>> Question.objects.all()
>>> from django.utils import timezone
>>> q = Question(question_text="What's new?", pub_date=timezone.now())
>>> q.save()
>>> q.id
>>> q.question_text
>>> q.pub_date
>>> q.question_text = "What's up?"
>>> q.save()
>>> Question.objects.all()
[<Question: Question object>]

<Question: Question object>对于这个对象是一个完全没有意义的表示。修复这个问题，编辑Question模型（在polls/models.py文件中）并添加一个__str__方法
在模型中添加__str__()方法很重要，不仅可以在命令交互时看的更方便，而且会在Django自动生成的管理界面中使用对象的这种表示。
'''