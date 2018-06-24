# _51job

## 1. 投递次数超过3次故障排查
* requests.exceptions.ConnectionTimeout
* requests.exceptions.ConnectionError
* requests.exceptions.ReadtTimeoutError

异常1表示，连接服务器超时；2表示已连上，但是服务器主动断开了连接；3表示，已连上，读取服务器发送过来的数据超时。

2的触发场景一般为，服务端检测参数不正确，就直接丢弃请求；触发到了i.51job.com和m.51job.com，并且发现这两个服务的地址都在同一台服务器上。

通过更换iP解决了投递的问题。