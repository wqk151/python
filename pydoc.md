## 01.简洁的表达式
##### 快速构建一个字典序列
```python
In [19]: dict(zip('abcd',range(4)))
Out[19]: {'a': 0, 'b': 1, 'c': 2, 'd': 3}
```
##### 用类似3目运算输出
```
In [22]: 'ok' if a==1 else 'ko'
Out[22]: 'ko'
```
##### 直接return 条件判断
```
def test(m):
    return 'a' if m==1 else 'b'
```
##### 推到列表生成字典
```
In [38]: list1 = ((1,'a'),(2,'b'))

In [39]: {x[0]:x[1] for x in list1}
Out[39]: {1: 'a', 2: 'b'}
```
## 02.排序
```python
In [27]: import heapq

#对列表
In [28]: nums = [10,2,9,100,80]

In [29]: heapq.nlargest(3,nums)
Out[29]: [100, 80, 10]

In [30]: heapq.nlargest(1,nums)
Out[30]: [100]

In [31]: heapq.nsmallest(3,nums)
Out[31]: [2, 9, 10]

# 对字典
In [33]: students = [{'name':'cc','score':100,'height':189},
                     {'name':'bb','score':10,'height':199},
                     {'name':'aa','score':90,'height':179}]

In [34]: heapq.nsmallest(2,students,key=lambda x:x['height'])
Out[34]:
[{'height': 179, 'name': 'aa', 'score': 90},
 {'height': 189, 'name': 'cc', 'score': 100}]
```
注：这个heapq库非常好用，尤其是我们在取一些列表的头部数据，比如最大几个，最小几个经常用到。

## 03.过滤

##### 用lambda配合filter过滤
```python
In [35]: list1 = ['to_pickle','to_recoreds','to_sql','valuese','update','mysql']

In [37]: list(filter(lambda x:x.startswith('to'),list1))
Out[37]: ['to_pickle', 'to_recoreds', 'to_sql']
```
注：Python3中filter生成的是迭代器

```
#用正则过滤
In [57]: list1 = ['to_pickle','to_recoreds','to_sql','valuese','update','mysql']

In [60]: list(filter(lambda x:re.findall('^to_',x),list1))
Out[60]: ['to_pickle', 'to_recoreds', 'to_sql']

#如果列表里面是一个个字典
In [61]: list2 = [{'aa':100,'bb':200},{'a1':300,'b1':400}]

In [62]: list(filter(lambda x:'aa' in x.keys(),list2))
Out[62]: [{'aa': 100, 'bb': 200}]
```

## 04.碾平list

##### 1)传统方法
```
s = [1,[2,[3,4]]]
res = []
def fun(s):
    for i in s:
        if isinstance(i,list):
            fun(i)
        else:
            res.append(i)
func(s)
print(res)
```
## 05.带条件的推导列表
```
#一个条件
In [63]: [x/2 for x in range(10) if x%2==0]
Out[63]: [0.0, 1.0, 2.0, 3.0, 4.0]

#多条件
In [64]: [x for x in range(30) if x%2==0 and x%6==0]
Out[64]: [0, 6, 12, 18, 24]

#用if-else
In [65]: [x+1 if x>=5 else x*10 for x in range(10)]
Out[65]: [0, 10, 20, 30, 40, 6, 7, 8, 9, 10]

#嵌套推导列表
In [66]: list_of_list = [[1,2,3],[4,5,6],[7,8,9]]

In [67]: [y for x in list_of_list for y in x]
Out[67]: [1, 2, 3, 4, 5, 6, 7, 8, 9]

```
## 06.更新字典
```python
In [68]: options = {'code':'utf-8'}

In [69]: base_headers = {"User-Agent":100,'Accept-Encoding':'gzip,sdch','Accept-Language':'zh-Cn,zh'}

# dict 会生成一个新的字典
In [70]: headers = dict(base_headers,**options)

In [71]: headers
Out[71]:
{'Accept-Encoding': 'gzip,sdch',
 'Accept-Language': 'zh-Cn,zh',
 'User-Agent': 100,
 'code': 'utf-8'}
 
# 或者使用update，更新原来的字典
In [74]: base_headers.update(options)

In [75]: base_headers
Out[75]:
{'Accept-Encoding': 'gzip,sdch',
 'Accept-Language': 'zh-Cn,zh',
 'User-Agent': 100,
 'code': 'utf-8'}

# 使用collection模块的defaultdict方法
In [76]: from collections import defaultdict

In [77]: dic = defaultdict(dict)

In [78]: dic['k1'].update({'k2':'aaa'})

In [79]: dic
Out[79]: defaultdict(dict, {'k1': {'k2': 'aaa'}})
虽然字典中没有键值k1，但仍然可以执行字典的update方法。
```
## 07.使用with忽视异常（仅限Python3）
from contextlib import ignored  # Python 3 only
with ignored(OSError):
    os.remove("somefile.txt")
