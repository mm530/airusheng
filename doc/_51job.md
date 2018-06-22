# _51job

## 1. 投递次数超过3次故障排查
投递过程中，已经创建了tcp连接，远程主机强迫关闭了一个现有的连接。

用socket连接i.51job.com的443端口，发现，socket长时间运行但是没有读取到服务端socket发送过来的数据，首先从运行结果来
说，程序没有报错，那么说明，已经成功建立连接，那为什么程序一直处于等待状态？服务端一直不写数据过来，我这边就一直
等待数据，所以就造成了这种情况。最终的结论就是，连接已经建立，等待服务器发送数据，而服务端一直不发送数据。服务端
不发数据过来，证明了，确实是在服务端封了IP。服务端接收到这个请求之后，直接就丢弃了。就这么简单的事情。一开始我以为
是硬件防火墙的问题。但是，也不能确定是不是封IP，假设是封账号呢？因为，我在手机上也测试过，手机上是可以让我成功提交的，
那就是说，封的还是IP了。还有一个需要考虑的是，用手机的接口做下测试，如果能，就说明只是针对了PC端的网页进行了限制。

隔了一个晚上之后，再去试试，注意，不要并发访问，先手工测试，如果发现能够成功请求，则表示，确实是封的IP。为了减轻
服务端的压力，这次我决定试试批量投递的接口。经过这次测试，还是不能成功请求，那么说明，这是封了账号了。但是，我的账号
在移动端确是能够成功访问的，那么，这时候，我可以试试用模拟移动端的方式来试试。

183.62.207.202 记住今天测试的IP.

分别在360浏览器和火狐浏览器上安装user agent switch 这个插件然后修改浏览器默认请求头，然后访问m.51job.com 443端口
发现，服务器丢弃了这个请求，打不开网页。

另外今天要找出批量接口的请求方式。

这是请求地址
```
https://i.51job.com/delivery/delivery.php?rand=0.4838858831437891&jsoncallback=jQuery18309977296096096169_1529629370861&jobid=(103694161%3A0%2C103686203%3A0)&prd=search.51job.com&prp=01&cd=search.51job.com&cp=01&resumeid=&cvlan=&coverid=&qpostset=&elementname=delivery_jobid&deliverytype=2&deliverydomain=%2F%2Fi.51job.com&language=c&imgpath=%2F%2Fimg03.51jobcdn.com&_=1529629376314
```
请求头
```
Accept:*/*
Referer:https://search.51job.com/list/040000,000000,0000,00,9,99,python,2,1.html?lang=c&stype=&postchannel=0000&workyear=99&cotype=99&degreefrom=99&jobterm=99&companysize=99&providesalary=99&lonlat=0%2C0&radius=-1&ord_field=0&confirmdate=9&fromType=&dibiaoid=0&address=&line=&specialarea=00&from=&welfare=
User-Agent:Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36
```

通过火狐代理设置插件及免费代理测试移动网站，确定是封了IP。

现在知道，i.51job.com和m.51job.com这两个域名都是封IP的，首先因为封IP的域名是i.51job.com，我对
m.51job.com并没有做什么，而m.51job.com却也封了IP，那说明一个问题，m.51job.com和i.51job.com这两个
服务是部署在一台服务器上的。排除了封账号的可能。

另外search.51job.com应该也是封ip的，只不过因为我的访问频率不高，所以没有触发条件。

逆水寒 礼包代码

YY02-2438-1954-7245

FA00-2362-5866-9879
