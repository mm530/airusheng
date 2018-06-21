import requests
import re
import time
import random
from lxml import etree
from threading import Thread
import os
import os.path
import pika
from PIL import Image
from io import BytesIO
import pickle
import logging
import socket

_51_ACCOUNT = '15800223273'
_51_PASSWD = 'sc5201314'
KEYWORD = 'python'

FILTER_COMPANY = ['天泰', '猎芯', '有棵树']
FILTER_JOB_NAME = ['人工智能', '数据分析', 'java', 'Java', '大数据', '异地']


class _51Job:
    init_count = 0
    init_timeout = 5
    def __init__(self):
        self.init_count += 1
        if self.init_count > 3:
            raise Exception('打开主页面，超时重试超过3次')
        headers = {
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
            'Accept-Encoding': 'gzip, deflate, br',
            'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
            'Cache - Control': 'max - age = 0',
            'Connection': 'keep-alive',
            'Host': '51job.com',
            'Upgrade-Insecure-Requests': '1',
            'User-Agent': 'Mozilla/5.0 (Macintosh1; Intel Mac OS X 10_13_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.139 Safari/537.36'
        }
        self.session = requests.Session()
        adapter = requests.adapters.HTTPAdapter(pool_connections=100, pool_maxsize=100)
        self.session.mount('http://', adapter)
        self.session.mount('https://', adapter)
        try:
            r = self.session.get('https://51job.com/', headers=headers, timeout=self.init_timeout)
        except requests.exceptions.ReadTimeout as e:
            self.init_timeout += 5
            self.__init__()
        except requests.exceptions.ConnectionError as e: # 远程主机强迫关闭了一个现有的连接
            self.__init__()
        else:
            r.raise_for_status()

    login_count = 0
    login_timeout = 5
    def login(self):
        if self.login_count > 3:
            raise Exception('提交登录表单，超时重试超过3次')
        headers = {
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
            'Accept-Encoding': 'gzip, deflate, br',
            'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
            'Cache-Control': 'max-age=0',
            'Connection': 'keep-alive',
            'Content-Length': '95',
            'Content-Type': 'application/x-www-form-urlencoded',
            'Host': 'login.51job.com',
            'Origin': 'https://www.51job.com',
            'Referer': 'https://www.51job.com/'
        }
        form_data = {
            'action': 'save',
            'from_domain': 'i',
            'lang': 'c',
            'loginname': _51_ACCOUNT,
            'password': _51_PASSWD,
            'verifycode': '',
            'isread': 'on'
        }
        try:
            r = self.session.post('https://login.51job.com/ajax/login.php', headers=headers, timeout=self.login_timeout, data=form_data)
        except requests.exceptions.ReadTimeout as e:
            self.logout_count += 1
            self.login_timeout += 5
            self.login()
        except requests.exceptions.ConnectionError as e:
            self.login()
        else:
            r.raise_for_status()
            r.encoding = 'gbk'
            if '"result":"1"' not in r.text:
                raise Exception('登录失败')

    _51job_com_count = 0
    _51job_com_timeout = 5
    def _51job_com(self):
        if self._51job_com_count > 3:
            raise Exception('登录成功之后访问主页重试超过3次')
        headers = {
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
            'Accept-Encoding': 'gzip, deflate, br',
            'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
            'Connection': 'keep-alive',
            'Host': 'www.51job.com',
            'Referer': 'https://www.51job.com/',
            'Upgrade-Insecure-Requests': '1',
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.139 Safari/537.36',
        }
        try:
            r = self.session.get('https://www.51job.com/', headers=headers, timeout=self._51job_com_timeout)
        except requests.exceptions.ReadTimeout as e:
            self._51job_com_count += 1
            self._51job_com_timeout += 5
            self._51job_com()
        except requests.exceptions.ConnectionError as e:
            self._51job_com()
        else:
            r.raise_for_status()
            r.encoding = 'gbk'
            if '我的51Job' not in r.text:
                raise Exception('我的51Job不在html源码里')

    search_count = 0
    search_timeout = 5
    def search(self, page=1, keyword='爬虫', session=False):
        if self.search_count > 100:
            raise Exception('搜索重试超过100次')
        url = requests.utils.requote_uri('https://search.51job.com/list/040000,000000,0000,00,9,07,' + keyword + ',2,' + str(page) + '.html?lang=c&stype=1&postchannel=0000&workyear=99&cotype=99&degreefrom=99&jobterm=99&companysize=99&lonlat=0%2C0&radius=-1&ord_field=0&confirmdate=9&fromType=21&dibiaoid=0&address=&line=&specialarea=00&from=&welfare=')
        print(url)
        headers = {
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
            'Accept-Encoding': 'gzip, deflate, br',
            'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
            'Connection': 'keep-alive',
            'Host': 'search.51job.com',
            'Referer': url,
            'Upgrade-Insecure-Requests': '1',
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.139 Safari/537.36',
        }
        try:
            if session:
                r = self.session.get(url, headers=headers, timeout=self.search_timeout)
            else:
                r = requests.get(url, headers=headers, timeout=self.search_timeout)
        except requests.exceptions.ReadTimeout as e:
            self.search_count += 1
            self.search_timeout += 5
            self.search(page, keyword, session)
        except requests.exceptions.ConnectionError as e:
            self.search(page, keyword, session)
        else:
            r.raise_for_status()
            r.encoding = 'gbk'
            html = etree.HTML(r.text)
            els = html.xpath('//div[@id="resultList"]/div[@class="el"]')
            jus = []

            err_count = 0
            for el in els:
                try:
                    company_name = el.xpath('./span[@class="t2"]/a/text()')[0].strip()
                    company_url = el.xpath('./span[@class="t2"]/a/@href')[0].strip()
                    company_addr = el.xpath('./span[@class="t3"]/text()')[0].strip()
                    publish_date = el.xpath('./span[@class="t5"]/text()')[0].strip()
                    job_name = el.xpath('./p[@class="t1 "]/span/a/text()')[0].strip()
                    job_url = el.xpath('./p[@class="t1 "]/span/a/@href')[0].strip()
                    job_id = el.xpath('./p[@class="t1 "]/input/@value')[0].strip()

                    filter_count = 0
                    for filter_company in FILTER_COMPANY:
                        if filter_company in company_name:
                            filter_count += 1
                    for filter_job_name in FILTER_JOB_NAME:
                        if filter_job_name in job_name:
                            filter_count += 1
                    if filter_count == 0:
                        jus.append([job_id, job_url])

                except Exception as e:
                    err_count += 1
                    if err_count == 1:
                        if not os.path.exists('51job'):
                            os.mkdir('51job')
                        with open('51job' + os.path.sep + str(time.time()) + '.log', 'w') as f:
                            f.write(r.text)
                    continue

            if page == 1:
                match = re.compile('共\d+页')
                m = match.search(r.text)
                self.total_page = int(m.group()[1:-1])
        
            return jus

    def delivery(self, job_id, job_url):
        delivery_count = 0
        delivery_timeout = 5

        def _delivery(job_id, job_url, delivery_count, delivery_timeout):
            delivery_count += 1
            if delivery_count > 3:
                raise Exception('投递次数超过3次')
            url = 'https://i.51job.com//delivery/delivery.php?rand=' + str(random.random()) + '&jsoncallback=jsonp' + str(int(time.time())) + '&_=' + str(int(time.time())) + '&jobid=(' + job_id +':0)&prd=search.51job.com&prp=01&cd=jobs.51job.com&cp=01&resumeid=&cvlan=&coverid=&qpostset=&elementname=hidJobID&deliverytype=1&deliverydomain=//i.51job.com/&language=c&imgpath=//img06.51jobcdn.com/'
            headers = {
                'Accept': '*/*',
                'Referer': job_url,
                'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.139 Safari/537.36',
            }
            try:
                r = self.session.get(url, headers=headers, timeout=delivery_timeout)
                print('.', end='')
            except requests.exceptions.ReadTimeout as e:
                delivery_timeout += 5
                _delivery(job_id, job_url, delivery_count, delivery_timeout)
            except requests.exceptions.ConnectionError as e:
                _delivery(job_id, job_url, delivery_count, delivery_timeout)
            else:
                r.raise_for_status()
                r.encoding = 'gbk'
                logging.log(logging.DEBUG, r.text)
                if '投递成功' not in r.text and '申请中包含已申请过的职位' not in r.text:
                    raise Exception('投递失败:' + r.text)
        _delivery(job_id, job_url, delivery_count, delivery_timeout)

    logout_count = 0
    logout_timeout = 5
    def logout(self):
        self.logout_count += 1
        if self.logout_count > 3:
            raise Exception('登出重试超过3次')
        url = 'https://login.51job.com/logout.php?lang=c'

        headers = {
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
            'Accept-Encoding': 'gzip, deflate, br',
            'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
            'Connection': 'keep-alive',
            'Host': 'login.51job.com',
            'Referer': 'https://www.51job.com/',
            'Upgrade-Insecure-Requests': '1',
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.139 Safari/537.36',
        }
        try:
            self.session.get(url, headers=headers)
        except requests.exceptions.ReadTimeout as e:
            self.logout_timeout += 5
            self.logout()
        except requests.exceptions.ConnectionError as e:
            self.logout()
        else:
            self.session.close()

    def download_captcha(self, session=False):
        count = 0
        timeout = 5
        def _download_captcha(count, timeout):
            count += 1
            if count > 3:
                raise Exception('下载图片重试超过3次')
            try:
                if session:
                    r = self.session.get('https://login.51job.com/ajax/verifycode.php', stream=True)
                else:
                    r = requests.get('https://login.51job.com/ajax/verifycode.php', stream=True)
            except requests.exceptions.ReadTimeout as e:
                timeout += 5
                _download_captcha(count, timeout)
            except requests.exceptions.ConnectionError as e:
                _download_captcha(count, timeout)
            else:
                r.raise_for_status()
                im = Image.open(BytesIO(r.content))
                if not os.path.exists('51job_captcha'):
                    os.mkdir('51job_captcha')
                im.save('51job_captcha' + os.path.sep + str(time.time()) + '.jpg')

        _download_captcha(count, timeout)


AMQP_USER = 'guest'
AMQP_PASS = 'guest'
AMQP_HOST = 'localhost'


def distribute_delivery():
    credentials = pika.PlainCredentials(AMQP_USER, AMQP_PASS)
    conn = pika.BlockingConnection(pika.ConnectionParameters(host=AMQP_HOST, credentials=credentials))
    ch = conn.channel()
    ch.queue_declare('delivery', durable=True)

    sp = _51Job()
    sp.login()
    keyword = KEYWORD
    sp._51job_com()
    jus = sp.search(page=1, keyword=keyword, session=True)
    print('总页数:', sp.total_page)
    spp = pickle.dumps(sp)

    for ju in jus:
        body = pickle.dumps([spp, ju])
        ch.basic_publish(exchange='', routing_key='delivery', properties=pika.BasicProperties(delivery_mode=2), body=body)
    print('第1页任务结束')

    for i in range(2, sp.total_page + 1):
        jus = sp.search(page=i, keyword=keyword, session=True)
        for ju in jus:
            body = pickle.dumps([spp, ju])
            ch.basic_publish(exchange='', routing_key='delivery', properties=pika.BasicProperties(delivery_mode=2), body=body)
        print('第%d页任务结束' % i)

    ch.close()
    conn.close()


def do_delivery_task():
    try:
        credentials = pika.PlainCredentials(AMQP_USER, AMQP_PASS)
        conn = pika.BlockingConnection(pika.ConnectionParameters(host=AMQP_HOST, credentials=credentials))
        ch = conn.channel()

        ch.queue_declare('delivery', durable=True)
        ch.basic_qos(prefetch_count=1)

        def callback(ch, method, properties, body):
            def task(ch, method, body):
                spj = pickle.loads(body)
                pickle.loads(spj[0]).delivery(spj[1][0], spj[1][1])
                ch.basic_ack(delivery_tag=method.delivery_tag)
            try:
                Thread(target=task, args=(ch, method, body)).start()
            except Exception as e:
                if '投递失败' not in str(e):
                    ch.basic_publish(exchange='', routing_key='delivery', properties=pika.BasicProperties(delivery_mode=2), body=body)

        ch.basic_consume(callback, queue='delivery', no_ack=False)
        ch.start_consuming()
        ch.close()
        conn.close()
    except pika.exceptions.ConnectionClosed as e:
        print(e)
        do_delivery_task()


def local_test():
    now = time.time()
    sp = _51Job()
    sp.login()
    keyword = KEYWORD
    sp._51job_com()
    jus = sp.search(page=1, keyword=keyword, session=True)
    print('总页数:', sp.total_page)

    ji = 0
    while ji < len(jus):
        sp.delivery(jus[ji][0], jus[ji][1])
        ji += 1

    print('\n第1页任务结束')
    
    for i in range(2, sp.total_page + 1):
        ts = []
        ji = 0
        jus = sp.search(page=i, keyword=keyword, session=True)
        while ji < len(jus):
            sp.delivery(jus[ji][0], jus[ji][1])
            if ji == len(jus) - 1:
                print('.')
            ji += 1
        print('\n第%d页任务结束' % i)

    sp.logout()
    print('总共用时:', time.time() - now)


def check_i_51job_com():
    s = socket.socket()
    s.settimeout(15)
    sig = s.connect_ex(('i.51job.com', 443))
    if sig != 0:
        raise Exception('连接异常')

    print(s.recv(1024).decode())

    s.close()