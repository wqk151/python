# -*- coding: utf-8 -*-
from django.test import TestCase
import datetime
from django.utils import timezone
from .models import Question
from django.core.urlresolvers import reverse
# Create your tests here.
# 自动化测试
# polls应用中有一个小错误：如果Question在最近一天发布，Question.was_published_recently()方法返回True，但是如果Question的pub_date字段是在未来，它还返回True（这是不对的）
#创建一个django.test.TestCase子类，它具有一个方法可以创建一个pub_date在未来的Question实例。然后检查was_published_recently()的输出--它应该是False。
class QuestionMethodTests(TestCase):
    def test_was_published_recently_with_future_question(self):
        time = timezone.now() + datetime.timedelta(days=30)
        future_question = Question(pub_date=time)
        self.assertEqual(future_question.was_published_recently(),False)
    def test_was_published_recently_with_old_question(self):
        time = timezone.now() - datetime.timedelta(days=30)
        old_question = Question(pub_date=time)
        self.assertEqual(old_question.was_published_recently(),False)
    def test_was_published_recently_with_recent_question(self):
        time = timezone.now() - datetime.timedelta(hours=1)
        recent_question = Question(pub_date=time)
        self.assertEqual(recent_question.was_published_recently(),True)

"""
运行测试：
python manage.py test polls
第一个测试用例发生了如下这些事：
1、python manage.py test polls查找polls应用下的测试用例
2、它找到django.test.TestCase类的子类
3、它为测试创建了一个特定的数据库
4、他查找用于测试的方法--名字以test开始
5、它运行test_was_published_recently_with_future_question创建一个pub_date未来30的Question实例
6、然后利用assertEqual()方法，它发现was_published_recently()返回True，尽管我们希望它返回False。
这个测试通知我们哪个测试失败，错误出现在哪一行。
##
为了防止修复一个错误的时候引入一个新的错误，在同一个类中添加两个其它的测试方法，来更加综合地测试这个方法。
现在有三个测试来包装无论发布时间是在过去、现在还是未来Question.was_published_recently()都将返回合理的数据。
Django提供了一个测试客户端来模拟用户和代码的交互。我们可以在tests.py甚至在shell中使用它。
在shell中设置测试环境：
>>>from django.test.utils import setup_test_environment
>>>setup_test_environment()
setup_test_environment()安装一个模板渲染器，可以使我们来检查响应的一些额外属性比如response.context,否则是访问不到的。
注意：这种方法不会建立一个测试数据库，所以一下命令将运行在现有的数据库上，输出的内容也会根据已经创建的Question不同而稍有不同。
下一步我们需要导入测试客户端类（在之后的tests.py中，我们将使用django.test.TestCase类，它具有自己的客户端，将不需要导入这个类）：
>>>from django.test import Client
>>>client = Client()
"""
# 测试新视图
# 创建一个快捷函数来创建Question，同时创建一个新的测试类
def create_question(question_text,days):
    time = timezone.now() + datetime.timedelta(days=days)
    return Question.objects.create(question_text=question_text,pub_date =time)

class QuestionViewTests(TestCase):
    def test_index_view_with_no_questions(self):
        response = self.client.get(reverse('polls:index'))
        self.assertEqual(response.status_code,200)
        self.assertContains(response,'No polls are available.')
        self.assertQuerysetEqual(response.context['latest_question_list'])
    def test_index_view_with_a_past_question(self):
        create_question(question_text="Past question.",days=-30)
        response = self.client.get(reverse('polls:index'))
        self.assertQuerysetEqual(
            response.context['latest_question_list'],
            ['<Question:Past question.>']
        )
    def test_index_view_with_a_future_question(self):
        pass





