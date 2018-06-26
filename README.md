# Lemon:让找工作更简单
![](https://github.com/mm530/lemon/raw/master/logo.jpg)

不敢说某某网站在信息方面对某一部分人进行了屏蔽，真实有效的信息往往被机器数据所掩盖，从大量脏数据中去寻找
那些你需要的数据时，手工显然不是做IT的范。Lemon，一个解决了51job.com上数据筛选和职位投递，并支持分布式单
个投递与批量投递的crawler更了解求职者的需求，愿意为您排忧解难。

这个库包含了这些功能：
* 自动登录
* 自动搜索
* 单个投递职位
* 批量投递职位
* 分布式单个投递职位
* 分布式批量投递职位

## 教程 & 使用
本地自动登录，搜索职位，过滤公司，职位名称，批量投递职位：
```python
from lemon import _51job

_51job._51ACCOUNT = 'xxx'
_51job._51PASSWD = 'xxx'
_51job.KEYWORD = 'xx职位'
_51job.FILTER_COMPANY = ['xx公司']
_51job.FILTER_JOB_NAME = ['xx工程师']

proxy_ips = []
_51job.local_many_test(proxy_ips)
```

更多信息，请看源码，或等文档更新。

## 安装
```bash
$ pip3 install git+https://github.com/mm530/lemon
```
该库仅仅支持Python3.6。
