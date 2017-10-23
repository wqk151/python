# -*- coding: utf-8 -*-
from django.shortcuts import get_object_or_404
from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from .models import Question
from .models import Choice
from django.views import generic
from django.utils import timezone
# Create your views here.
# 你的视图可以从数据库中读取记录，或者不读取数据库。你还可以动态地生成一个PDF文件、输出XML文件、创建一个Zip文件或者使用你想用Python库生成任何想要的形式。


# 导入model，可以操作数据库
class IndexView(generic.ListView):
    template_name = 'polls/index.html'
    context_object_name = 'latest_question_list'
    def get_queryset(self):
        """return the last five published questions."""
        return Question.objects.filter(pub_date__lte=timezone.now()).order_by('-pub_date')[:5]
#        return Question.objects.order_by('-pub_date')[:5]
# response.context_data['latest_question_list']取出由视图放置在context中的数据。
class DetailView(generic.DetailView):
    model = Question
    template_name = 'polls/detail.html'
    def get_queryset(self):
        return Question.objects.filter(pub_date__lte=timezone.now())
class ResultsView(generic.DetailView):
    model = Question
    template_name = 'polls/results.html'


def vote(request,question_id):
    p = get_object_or_404(Question, pk=question_id)
    try:
        selected_choice = p.choice_set.get(pk=request.POST['choice'])
    except (KeyError, Choice.DoesNotExist):
        # Redisplay the question voting form.
        return render(request, 'polls/detail.html', {
            'question': p,
            'error_message': "You didn't select a choice.",
        })
    else:
        selected_choice.votes += 1
        selected_choice.save()
        # Always return an HttpResponseRedirect after successfully dealing
        # with POST data. This prevents data from being posted twice if a
        # user hits the Back button.
        return HttpResponseRedirect(reverse('polls:results',args=(p.id,)))
"""
在vote视图函数中
1、request.POST是一个类似字典的对象，让你可以通过关键字名字获取提交的数据。这个例子中，request.POST['choice']以字符串形式返回选择的Choice的ID。
request.POST的值永远是字符串。
2、如果在POST数据中没有提供choice，request.POST['choice']将引发一个KeyError。上面的代码检查KeyError，如果没有给出choice将重新显示Question表单和错误信息。
3、在增加Choice的得票数之后，代码返回一个HttpResponseRedirect而不是常用的HttpResponse。
HttpResponseRedirect只接收一个参数：用户将要被重定向的URL。
你应该在成功处理POST数据后总数返回一个HttpResponseRedirect。
4、在这个例子中，我们在HttpResponseRedirect的构造函数中使用reverse()函数。这个函数避免了我们在视图函数中硬编码URL。
它需要我们给出我们想要跳转的视图名字和该视图所对应的URL模式中需要给该视图提供的参数。在本例中，使用在URLconf的配置，reverse()调用将返回一个这样的字符串：
'/polls/3/results'
其中3是p.id的值。重定向URL将调用'results'视图来显示最终的页面。
request是一个HttpRequest对象。详细参考：请求和响应的文档：http://python.usyiyi.cn/translate/django_182/ref/request-response.html

"""
"""
使用通用视图--减少代码
detail()、index()和resultes()视图都类似，存在冗余问题
这些视图反映基本的web开发中一个常见的情况：根据URL中的参数从数据库中获取数据、载入模板文件，然后返回渲染后的模板。
由于这种情况非常普遍，Django提供了一种叫做"generic views"的系统可以方便地进行处理。
Generic views会将常见的模式抽象化，可以使你在编写APP时，甚至不需要编写Python代码。
这里使用了两个通用视图：ListView和DetailView。这两个视图分别抽象"显示一个对象列表"和"显示一个特定对象的详细信息页面"这两种概念。
1、每个通用视图需要知道它将作用于哪个模型。这由model属性提供。
2、DetailView期望从URL中捕获名为'pk'的主键值，因此我们把polls/urls.py中的question_id改成了通用视图可以找到的主键值。
默认情况下，通用视图DetailView使用一个叫做<app name>/<model name>_detail.html的模板。在我们的例子中，它将使用"polls/question_detail.html"模板。
template_name属性是用来告诉Django使用一个指定的模板名字，而不是自动生成的默认名字。
类似地，ListView使用一个叫做<app name>/<model name>_list.html的默认模板；我们使用template_name来告诉ListView使用我们自己已经存在的"polls/index.html"模板。
之前教程中，提供模板文件时都带有一个包含question和latest_question_list变量的context。
对于DetailView，question变量会自动提供--因为我们使用Django的模型（question），Django能够为context变量决定一个合适的名字。
然而对于ListView，自动生成的context变量是question_list。为了覆盖这个行为，我们提供context_object_name属性，表示我们想使用latest_question_list，作为一种替换方案。
通用视图文档：http://python.usyiyi.cn/translate/django_182/topics/class-based-views/index.html

"""

