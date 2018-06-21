import requests
import lxml

ZL_TEL = '15800223273'
ZL_PASS = 'sc5201314'


class ZhiLian:

    init_count = 0
    init_timeout = 5
    def __init__(self):
        self.init_count += 1
        if self.init_count > 3:
            raise Exception('主页重试次数超过3次')

        url = 'https://www.zhaopin.com/#'
        headers = {
            'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Encoding':'gzip, deflate, sdch',
            'Accept-Language':'zh-CN,zh;q=0.8',
            'Cache-Control':'max-age=0',
            'Connection':'keep-alive',
            'Host':'www.zhaopin.com',
            'If-Modified-Since':'Thu, 21 Jun 2018 00:40:03 GMT',
            'If-None-Match':'W/"5b2af3e3-202e6"',
            'Upgrade-Insecure-Requests':'1',
            'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36',
        }
        self.session = requests.Session()
        adapter = requests.adapters.HTTPAdapter(pool_connections=100, pool_maxsize=100)
        self.session.mount('http://', adapter)
        self.session.mount('https://', adapter)
        try:
            r = self.session.get(url, headers=headers, timeout=self.init_timeout)
        except requests.exceptions.ReadTimeout as e:
            print(e)
            self.init_timeout += 5
            self.__init__()
        except requests.exceptions.ConnectionError as e:
            print(e)
            self.__init__()
        else:
            r.raise_for_status()
            r.encoding = 'utf-8'
            if '招聘_求职_找工作_上智联招聘人才网' not in r.text:
                raise Exception('主页返回数据不正常')

    login_count = 0
    login_timeout = 5
    def login(self):
        url = 'https://passport.zhaopin.com/account/login'
        headers = {
            'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Encoding':'gzip, deflate',
            'Accept-Language':'zh-CN,zh;q=0.8',
            'Cache-Control':'max-age=0',
            'Content-Length':'149',
            'Content-Type':'application/x-www-form-urlencoded',
            'Host':'passport.zhaopin.com',
            'Origin':'https://www.zhaopin.com',
            'Referer':'https://www.zhaopin.com/',
            'Upgrade-Insecure-Requests':'1',
            'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'
        }
        form_data = {
            'int_count':'999',
            'errUrl':'https://passport.zhaopin.com/account/login',
            'RememberMe':'true',
            'requestFrom':'portal',
            'loginname': ZL_TEL,
            'Password': ZL_PASS,
        }
        try:
            r = self.session.post(url, headers=headers, data=form_data, timeout=self.login_timeout)
        except requests.exceptions.ReadTimeout as e:
            self.login_timeout += 5
            self.login()
        except requests.exceptions.ConnectionError as e:
            self.login()
        else:
            r.raise_for_status()
            print(r.status_code)
            print(r.text)

    def logout(self):
        pass

    def search(self):
        pass

    def delivery(self):
        pass
