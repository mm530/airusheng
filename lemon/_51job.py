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
import socket
from requests.utils import OrderedDict

_51_ACCOUNT = 'YOUR TEL'
_51_PASSWD = 'YOUR PASS'
KEYWORD = 'python'

FILTER_COMPANY = ['天泰', '猎芯', '有棵树']
FILTER_JOB_NAME = ['人工智能', '数据分析', 'java', '大数据', '异地', 'ios']


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
            raise e
        else:
            r.raise_for_status()

    def check_verify_code(self, verifycode):
        retry_count = 0
        timeout = 5
        def _check_verify_code(retry_count, timeout):
            url = 'https://login.51job.com/ajax/checkcode.php'
            headers = {
                'Accept':'*/*',
                'Accept-Encoding':'gzip, deflate, br',
                'Accept-Language':'zh-CN,zh;q=0.9',
                'Host':'login.51job.com',
                'Referer':'https://www.51job.com/',
                'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36'
            }
            form_data = {
                'jsoncallback':'jQuery%d_%d' % (int(time.time()), int(time.time())),
                'verifycode': verifycode,
                'type':'3',
                'from_domain':'my',
                '_': str(int(time.time())),
            }
            try:
                r = self.session.get(url, headers=headers, timeout=timeout, params=form_data)
            except requests.exceptions.ConnectTimeout as e:
                retry_count += 1
                timeout += 5
                _check_verify_code(retry_count, timeout)
            except requests.exceptions.ReadTimeout as e:
                retry_count += 1
                timeout += 5
                _check_verify_code(retry_count, timeout)
            except requests.exceptions.ConnectionError as e:
                raise e
            else:
                r.encoding = 'utf-8'
                print('--------', r.text)
                if '"result":1' not in r.text:
                    raise Exception('验证码错误')
        _check_verify_code(retry_count, timeout)

    login_count = 0
    login_timeout = 5
    def login(self, proxies={}):
        if self.login_count > 3:
            raise Exception('提交登录表单，超时重试超过3次')
        headers = {
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
            'Accept-Encoding': 'gzip, deflate, br',
            'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
            'Cache-Control': 'max-age=0',
            'Content-Length': '95',
            'Content-Type': 'application/x-www-form-urlencoded',
            'Host': 'login.51job.com',
            'Origin': 'https://www.51job.com',
            'Referer': 'https://www.51job.com/',
            'Upgrade-Insecure-Requests': '1',
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.139 Safari/537.36',
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
            r = self.session.post('https://login.51job.com/ajax/login.php', headers=OrderedDict(headers), timeout=self.login_timeout, data=form_data, proxies=proxies)
        except requests.exceptions.ReadTimeout as e:
            self.login_count += 1
            self.login_timeout += 5
            self.login()
        except requests.exceptions.ConnectTimeout as e:
            self.login_count += 1
            self.login_timeout += 5
            self.login()
        except requests.exceptions.ConnectionError as e:
            self.login_count += 1
            self.login_timeout += 5
            self.login()
        else:
            r.raise_for_status()
            r.encoding = 'gbk'
            if '"result":"1"' not in r.text:
                if not os.path.exists('51job'):
                    os.mkdir('51job')
                with open('51job' + os.path.sep + 'login_' + str(time.time()) + '.log', 'w', encoding='gbk') as f:
                    f.write(r.text)
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
        except requests.exceptions.ConnectTimeout as e:
            self._51job_com_count += 1
            self._51job_com_timeout += 5
            self._51job_com()
        except requests.exceptions.ConnectionError as e:
            raise Exception('服务器接收到请求之后，丢弃了这个连接')
        else:
            r.raise_for_status()
            r.encoding = 'gbk'
            if '我的51Job' not in r.text:
                raise Exception('我的51Job不在html源码里')

    search_count = 0
    search_timeout = 5
    def search(self, page=1, keyword='爬虫', session=False, many=False):
        '''
        如果是非批量投递，则返回[[job_id, job_url],...,n]，否则返回[job_id,...,n], so_url
        '''
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
            self.search(page, keyword, session, many)
        except requests.exceptions.ConnectTimeout as e:
            self.search_count += 1
            self.search_timeout += 5
            self.search(page, keyword, session, many)
        except requests.exceptions.ConnectionError as e:
            raise Exception('服务器接收到请求后，主动断开了连接')
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
                    # company_url = el.xpath('./span[@class="t2"]/a/@href')[0].strip()
                    # company_addr = el.xpath('./span[@class="t3"]/text()')[0].strip()
                    # publish_date = el.xpath('./span[@class="t5"]/text()')[0].strip()
                    job_name = el.xpath('./p[@class="t1 "]/span/a/text()')[0].strip()
                    job_url = el.xpath('./p[@class="t1 "]/span/a/@href')[0].strip()
                    job_id = el.xpath('./p[@class="t1 "]/input/@value')[0].strip()

                    filter_count = 0
                    for filter_company in FILTER_COMPANY:
                        if filter_company.lower() in company_name.lower():
                            filter_count += 1
                    for filter_job_name in FILTER_JOB_NAME:
                        if filter_job_name.lower() in job_name.lower():
                            filter_count += 1
                    if filter_count == 0:
                        if not many:
                            jus.append([job_id, job_url])
                        else:
                            jus.append(job_id)

                except Exception as e:
                    err_count += 1
                    if err_count == 1:
                        if not os.path.exists('51job'):
                            os.mkdir('51job')
                        with open('51job' + os.path.sep + 'delivery_' + str(time.time()) + '.log', 'w', encoding='gbk') as f:
                            f.write(r.text)
                    continue

            if page == 1:
                match = re.compile('共\d+页')
                m = match.search(r.text)
                self.total_page = int(m.group()[1:-1])

            if not many:
                return jus
            else:
                return jus, url

    def delivery(self, job_id, job_url, proxies={}):
        delivery_count = 0
        delivery_timeout = 30

        def _delivery(job_id, job_url, delivery_count, delivery_timeout, proxies):
            if delivery_count > 3:
                raise Exception('投递次数超过3次')
            url = 'https://i.51job.com/delivery/delivery.php'
            form_data = {
                '_': int(time.time()),
                'cd':'search.51job.com',
                'coverid': '',
                'cp': '01',
                'cvlan': '',
                'deliverydomain': '//i.51job.com',
                'deliverytype': '2',
                'elementname': 'delivery_jobid',
                'imgpath': '//img06.51jobcdn.com',
                'jobid': '(' + job_id + ':0)',
                'jsoncallback': 'jQuery%d_%d' % (int(time.time()), int(time.time())),
                'language': 'c',
                'prd': 'search.51job.com',
                'prp': '01',
                'qpostset':'',
                'rand': random.random(),
                'resumeid': '',
            }
            headers = {
                'Accept': '*/*',
                'Accept-Encoding': 'gzip, deflate, br',
                'Accept-Language': 'zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2',
                'Host': 'i.51job.com',
                'Referer': job_url,
                'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.139 Safari/537.36',
            }
            try:
                r = self.session.get(url, headers=OrderedDict(headers), timeout=delivery_timeout, params=form_data)
            except requests.exceptions.ReadTimeout as e:
                delivery_count += 1
                delivery_timeout += 5
                _delivery(job_id, job_url, delivery_count, delivery_timeout, proxies)
            except requests.exceptions.ConnectTimeout as e:
                delivery_count += 1
                delivery_timeout += 5
                _delivery(job_id, job_url, delivery_count, delivery_timeout, proxies)
            except requests.exceptions.ConnectionError as e:
                raise Exception('服务器接收到这个请求，但是主动断开了连接')
            else:
                r.raise_for_status()
                r.encoding = 'gbk'
                print('delivery log:', r.text)
                if '投递成功' not in r.text and '申请中包含已申请过的职位' not in r.text:
                    raise Exception('投递失败:' + r.text)
        _delivery(job_id, job_url, delivery_count, delivery_timeout, proxies)

    def delivery_many(self, job_ids, so_url, proxies={}):
        delivery_count = 0
        delivery_timeout = 30

        def _delivery_many(job_ids, so_url, delivery_count, delivery_timeout, proxies):
            if delivery_count > 3:
                raise Exception('投递次数超过3次')
            job_id_str = ''
            for ji in job_ids:
                job_id_str = str(ji) + ':' + '0,'
            job_id_str = job_id_str[:-1]
            url = 'https://i.51job.com/delivery/delivery.php'
            form_data = {
                '_': int(time.time()),
                'cd': 'search.51job.com',
                'coverid': '',
                'cp': '01',
                'cvlan': '',
                'deliverydomain': '//i.51job.com',
                'deliverytype': '2',
                'elementname': 'delivery_jobid',
                'imgpath': '//img06.51jobcdn.com',
                'jobid': '(' + job_id_str + ')',
                'jsoncallback': 'jQuery%d_%d' % (int(time.time()), int(time.time())),
                'language': 'c',
                'prd': 'search.51job.com',
                'prp': '01',
                'qpostset': '',
                'rand': random.random(),
                'resumeid': '',
            }
            headers = {
                'Accept': '*/*',
                'Accept-Encoding': 'gzip, deflate, br',
                'Accept-Language': 'zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2',
                'Host': 'i.51job.com',
                'Referer': so_url,
                'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.139 Safari/537.36',
            }
            try:
                r = self.session.get(url, headers=headers, timeout=delivery_timeout, proxies=proxies, params=form_data)
            except requests.exceptions.ReadTimeout as e:
                delivery_count += 1
                delivery_timeout += 5
                _delivery_many(job_ids, so_url, delivery_count, delivery_timeout, proxies)
            except requests.exceptions.ConnectTimeout as e:
                delivery_count += 1
                delivery_timeout += 5
                _delivery_many(job_ids, so_url, delivery_count, delivery_timeout, proxies)
            except requests.exceptions.ConnectionError as e:
                raise Exception('服务器接收到这个请求，但是主动断开了连接')
            else:
                r.raise_for_status()
                r.encoding = 'gbk'
                print(r.text)
                if '申请中包含已申请过的职位' not in r.text and '成功' not in r.text:
                    raise Exception('批量申请失败')
        _delivery_many(job_ids, so_url, delivery_count, delivery_timeout, proxies)

    logout_count = 0
    logout_timeout = 5
    def logout(self):
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
            self.logout_count += 1
            self.logout_timeout += 5
            self.logout()
        except requests.exceptions.ConnectTimeout as e:
            self.logout_count += 1
            self.logout_timeout += 5
            self.logout()
        except requests.exceptions.ConnectionError as e:
            raise Exception('服务器接收了这个请求，但是主动断开了连接')
        else:
            self.session.close()

    def download_captcha(self, session=False, debug=False):
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
            except requests.exceptions.ConnectTimeout as e:
                timeout += 5
                _download_captcha(count, timeout)
            except requests.exceptions.ConnectionError as e:
                raise e
            else:
                r.raise_for_status()
                im = Image.open(BytesIO(r.content))
                if not os.path.exists('51job_captcha'):
                    os.mkdir('51job_captcha')
                im.save('51job_captcha' + os.path.sep + str(time.time()) + '.jpg')

                if debug:
                    im.show()

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


def distribute_delivery_many():
    credentials = pika.PlainCredentials(AMQP_USER, AMQP_PASS)
    conn = pika.BlockingConnection(pika.ConnectionParameters(host=AMQP_HOST, credentials=credentials))
    ch = conn.channel()
    ch.queue_declare('delivery', durable=True)

    sp = _51Job()
    sp.login()
    keyword = KEYWORD
    sp._51job_com()
    ju = sp.search(page=1, keyword=keyword, session=True, many=True)
    print('总页数:', sp.total_page)
    spp = pickle.dumps(sp)

    body = pickle.dumps([spp, ju])
    ch.basic_publish(exchange='', routing_key='delivery_many', properties=pika.BasicProperties(delivery_mode=2), body=body)
    print('第1页任务结束')

    for i in range(2, sp.total_page + 1):
        ju = sp.search(page=i, keyword=keyword, session=True, many=True)
        body = pickle.dumps([spp, ju])
        ch.basic_publish(exchange='', routing_key='delivery', properties=pika.BasicProperties(delivery_mode=2), body=body)
        print('第%d页任务结束' % i)

    ch.close()
    conn.close()

def do_delivery_task_many():
    try:
        credentials = pika.PlainCredentials(AMQP_USER, AMQP_PASS)
        conn = pika.BlockingConnection(pika.ConnectionParameters(host=AMQP_HOST, credentials=credentials))
        ch = conn.channel()

        ch.queue_declare('delivery', durable=True)
        ch.basic_qos(prefetch_count=1)

        def callback(ch, method, properties, body):
            def task(ch, method, body):
                spj = pickle.loads(body)
                pickle.loads(spj[0]).delivery_many(spj[1][0], spj[1][1])
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


def local_test(ips):
    '''
    单个投递，如果多线程弄，很容易导致对面数据库挂掉，直接就导致IP被封死。
    :param ips:
    :return:
    '''
    now = time.time()
    sp = _51Job()
    sp.login()
    keyword = KEYWORD
    sp._51job_com()
    jus = sp.search(page=1, keyword=keyword, session=True)
    print('总页数:', sp.total_page)

    ji = 0
    while ji < len(jus):
        proxies = {}
        if len(ips) > 0:
            index = random.randint(0, len(ips) - 1)
            proxies = {
                'http': 'http://' + ips[index].ip + ':' + ips[index].port,
                'https': 'http://' + ips[index].ip + ':' + ips[index].port,
            }
        try:
            sp.delivery(jus[ji][0], jus[ji][1], proxies=proxies)
        except:
            del ips[index]
            continue
        finally:
            time.sleep(10)
        ji += 1

    print('\n第1页任务结束')

    for i in range(2, sp.total_page + 1):
        ts = []
        ji = 0
        jus = sp.search(page=i, keyword=keyword, session=True)
        while ji < len(jus):
            if len(ips) > 0:
                index = random.randint(0, len(ips) - 1)
                proxies = {
                    'http': ips[index].type + '://' + ips[index].ip + ';' + ips[index].port,
                    'https': ips[index].type + '://' + ips[index].ip + ';' + ips[index].port,
                }
            try:
                sp.delivery(jus[ji][0], jus[ji][1], proxies=proxies)
            except:
                del ips[index]
                continue
            if ji == len(jus) - 1:
                print('.')
            ji += 1
        print('\n第%d页任务结束' % i)

    sp.logout()
    print('总共用时:', time.time() - now)


def local_many_test(ips):
    '''
    批量投递，有多少页就发送多少个投递请求，相对来说，效率是单个投递效率的50倍。封IP的几率大大降低。
    :param ips:
    :return:
    '''
    now = time.time()
    sp = _51Job()

    proxies = {}
    if len(ips) > 0:
        index = random.randint(0, len(ips) - 1)
        proxies = {
            'http': ips[index].type + '://' + ips[index].ip + ':' + ips[index].port,
            'https': ips[index].type + '://' + ips[index].ip + ':' + ips[index].port,
        }

    sp.login(proxies)
    sp._51job_com()
    jusu = sp.search(page=1, keyword=KEYWORD, session=True, many=True)
    print('总页数:', sp.total_page)

    proxies = {}
    if len(ips) > 0:
        index = random.randint(0, len(ips) - 1)
        proxies = {
            'http': ips[index].type + '://' + ips[index].ip + ':' + ips[index].port,
            'https': ips[index].type + '://' + ips[index].ip + ':' + ips[index].port,
        }

    sp.delivery_many(jusu[0], jusu[1], proxies=proxies)
    for page in range(2, sp.total_page + 1):
        jusu = sp.search(page=page, keyword=KEYWORD, session=True, many=True)

        proxies = {}
        if len(ips) > 0:
            index = random.randint(0, len(ips) - 1)
            proxies = {
                'http': ips[index].type + '://' + ips[index].ip + ';' + ips[index].port,
                'https': ips[index].type + '://' + ips[index].ip + ';' + ips[index].port,
            }
        sp.delivery_many(jusu[0], jusu[1], proxies=proxies)
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


def check_m_51job_com():
    s = socket.socket()
    s.settimeout(15)
    sig = s.connect_ex(('m.51job.com', 443))
    if sig != 0:
        raise Exception('连接异常')
    print(s.recv(1024).decode())
    s.close()


def check_proxy_i_51job_com(ip):
    url = 'https://i.51job.com'
    headers = {
        'Accept': '*/*',
        'Referer': url,
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.139 Safari/537.36',
    }
    proxies = {
        'http': 'http://' + ip.ip + ':' + ip.port,
        'https': 'http://' + ip.ip + ':' + ip.port,
    }
    try:
        r = requests.get(url, headers=headers, proxies=proxies, timeout=10)
    except Exception as e:
        return False
    else:
        r.encoding = 'utf-8'
        # print(r.text)
        return True


def account_init():
    global _51_PASSWD, _51_ACCOUNT, KEYWORD
    def input_apk():
        global _51_PASSWD, _51_ACCOUNT, KEYWORD
        _51_ACCOUNT = input('tel:')
        _51_PASSWD = input('pass:')
        KEYWORD = input('keyword:')

    cfg = os.path.expanduser('~') + os.path.sep + '.51job.conf'
    if os.path.exists(cfg):
        lines = None
        with open(cfg, 'r', encoding='utf-8') as f:
            lines = f.read()
        if lines:
            try:
                tmp = lines.split('~~~')
                _51_ACCOUNT = tmp[0]
                _51_PASSWD = tmp[1]
                KEYWORD = tmp[2]
            except Exception as e:
                input_apk()
        else:
            input_apk()
    else:
        input_apk()

    if _51_ACCOUNT is None or _51_PASSWD is None or KEYWORD is None:
        raise Exception('输入参数错误')
    else:
        with open(cfg, 'w') as f:
            f.write(_51_ACCOUNT + '~~~' + _51_PASSWD + '~~~' + KEYWORD)
