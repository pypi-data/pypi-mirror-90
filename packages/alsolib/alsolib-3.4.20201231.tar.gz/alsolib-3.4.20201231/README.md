
# alsolib v3.4
alsolib开发者：苦逼者钟宇轩

说明:本库为原创库，火焰工作室精心打造

版权所有，侵权必究


### alsolib 一个最重要的功能
想知道是谁在看你的学而思作品吗?
他来了~
```python
from alsolib.xes import*
a=getnowuser()
print(a) 
#正常:{'state':True,'user_id':"7821237", "user_name":"苦逼者钟宇轩"}
#未登录:{"state":False,'user_id':"未登录","user_name":"未登录"}
```


###alsolib(alsolib)主要库介绍说明
###注:alsolib介绍成功全为0，失败全为-1
内置函数 导入方式：

```python
from alsolib import *
```
百度百科

```python
a=baidubaike("***")
print(a)
```
翻译

```python
a=translate("Hello") 
print(a)
```
天气

```python
a=getweather("guangdong","guangzhou")#省，市的英文
print(a)
```

内置网页浏览器 title为自定义标题

```python
a=getweather("http://www.asunc.cn/","title")#一定要加http://或https://
print(a)
```

### 学而思库说明(alsolib.xes)
###注:alsolib.xes介绍成功全为0，失败全为-1
导入方式
```python
from alsolib.xes import*
a=LoadWork("一个作品的pid")
```


学而思获取作品赞

```python
b=a.get_likes()
print(b)
```

学而思获取作品作者

```python
b=a.get_user()
print(b)
```

学而思获取作品踩的数量

```python
b=a.get_unlikes()
print(b)
```

学而思获取作品介绍

```python
b=a.get_description()
print(b)
```

学而思获取作者信息

```python
b=a.get_name_as_pid()
print(b)
```

学而思获取你对这个作品点赞没有~

```python
while 1:
    b=a.is_like()
    if b==0:
	print("你点赞了")
    if b==-1:
	print("你踩了")
    if b==1:
	print("你没点赞也没踩")
```

### hyChat库(alsolib.hychat)

```python
import alsolib.hychat 
```
###api库(alsolib.api)

导库
```python
from alsolib.api import*
a=Alsoai()
```
1.获取IP地理位置:
```python
print(a.get_ipaddress(ip,get_point))
#第一个参数必填,第二个参数选填，填True后会返回城市名和这个城市的中心经纬度城市名
#不填或False则只返回城市名
#错误返回值为-1,成功为0
```
2.获取道路交通路况:
```python
print(a.get_traffic(road,city))
#全部参数都要填，会返回这个道路的路况，像堵车，畅通......
#错误返回值为-1,成功为0
```
3.制作AI音频:
```python
print(a.makevoice(text,filename,mode=1,speed=40))
#第一二个参数必填,三四个选填,第一个参数填入发音的文字，第二个参数填路径
#第三个参数填发音人(1为男人，5，6，7为三种不同声音的女人),第四个参数填声音范围(0-100)
#返回值成功为0，错误返回-1
```
4.AI语音:
```python
print(a.speak(text,mode=1,speed=40))
#第一个参数必填,二三个选填,第一个参数填入发音的文字,第二个参数填发音人
#(1为男人，5，6，7为三种不同声音的女人),第三个参数填声音范围(0-100)
#返回值成功为0，错误返回-1
```
5.AI智能聊天机器人:
```python
print(a.AI_chat(text,is_speak=False,mode=5))
#第一个参数必填,二三个选填,第一个参数传入你想对机器人说的话，第二个传入
#是否以AI说语音,第三个填发音人(1为男人，5，6，7为三种不同声音的女人)
#成功返回0,AI智能聊天机器人的回答，失败返回-1,404为操作太快
```

###结束:本介绍解释终归火焰工作室，感谢您的收看~~~



