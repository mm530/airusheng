# Lemon:让找工作更简单
![](https://github.com/mm530/lemon/raw/master/logo.jpg)

这个库是为了解决在51job.com上搜索职位时面临太多搜索结果而无法一一去审核并且珍惜那些宝贵的机会而开发的一款分布式的多线程的crawler。

当使用这个库时，你会自动获得这些:
* 自动登录
* 自动搜索
* 单个投递职位
* 批量投递职位
* 分布式单个投递职位
* 分布式批量投递职位
* 封IP的解决策略
* 验证码的破解

# 教程 & 使用
本地自动登录，搜索职位，单个投递职位：
```python
from lemon import _51job

_51job._51ACCOUNT = 'xxx'
_51job._51PASSWD = 'xxx'
_51job.KEYWORD = 'xx职位'

_51job.local_test([])
```

# 安装
```
$ pip3 install git+https://github.com/mm530/lemon
```
仅仅支持Python3.6。

神经网络的教程:
http://www.tensorfly.cn/index.html
