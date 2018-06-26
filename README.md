# Lemon:让找工作更简单
![](https://github.com/mm530/lemon/raw/master/logo.jpg)

Lemon，51job.com爬虫，让找工作变得更简单，节约您的时间。

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

## 待开发功能
- [ ] 投递职位封IP
- [ ] 训练登录验证码的神经网络模型
- [ ] 终端日志信息的完善

## 鸣谢
* Python
* Linux
* Pycharm
* requests
* lxml
* Pillow
* numpy