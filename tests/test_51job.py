from unittest import TestCase
from airusheng import _51job
import urllib.parse
from airusheng.proxy_ip import get_ips
import random
from threading import Thread
import os
from airusheng.proxy_ip import  IP


def get_checked_ip(ips):
    ok_ips = []
    def is_ok(ip):
        if _51job.check_proxy_i_51job_com(ip):
            ok_ips.append(ip)

    ts = []
    for ip in ips:
        t = Thread(target=is_ok, args=(ip,))
        t.start()
    for t in ts:
        t.join()

    return ok_ips


class Test(TestCase):
    def test_account_init(self):
        _51job.account_init()
        if os.path.exists('.51job.conf'):
            with open('.51job.conf', 'r') as f:
                print(f.read())
        print(_51job._51_ACCOUNT, _51job._51_PASSWD, _51job.KEYWORD)

    def test_local_test(self):
        _51job.account_init()
        ips = get_ips()
        ok_ips = get_checked_ip(ips)
        print('可以使用的IP有:%d个' % len(ok_ips), ok_ips)

        _51job.local_test(ok_ips)

    def test_local_test_do_not_use_proxy(self):
        _51job.account_init()
        _51job.local_test([])

    def test_distribute_delivery(self):
        _51job.account_init()
        _51job.distribute_delivery()

    def test_do_delivery_task(self):
        _51job.do_delivery_task()

    def test_check_i_51job_com(self):
        _51job.check_i_51job_com()

    def test_check_m_51job_com(self):
        _51job.check_m_51job_com()

    def test_view_batch_delivery_api(self):
        url = 'https://i.51job.com/delivery/delivery.php?rand=0.4838858831437891&jsoncallback=jQuery18309977296096096169_1529629370861&jobid=(103694161%3A0%2C103686203%3A0)&prd=search.51job.com&prp=01&cd=search.51job.com&cp=01&resumeid=&cvlan=&coverid=&qpostset=&elementname=delivery_jobid&deliverytype=2&deliverydomain=%2F%2Fi.51job.com&language=c&imgpath=%2F%2Fimg03.51jobcdn.com&_=1529629376314'
        print(urllib.parse.unquote(url))

    def test_local_many_test_use_special_proxy(self):
        _51job.account_init()
        ips = [
            IP('221.7.255.168', '80', 'http', None, None, None, None)
        ]
        _51job.local_many_test(ips)

    def test_local_many_test_do_not_use_proxy(self):
        _51job.account_init()
        _51job.local_many_test([])

    def test_download_capthca(self):
        sp = _51job._51Job()
        for i in range(100):
            sp.download_captcha()

    def test_check_proxy_i_51job_com(self):
        ips = get_ips()
        index = random.randint(0, len(ips) - 1)
        ip = ips[index]
        result = _51job.check_proxy_i_51job_com(ip)
        self.assertTrue(result)

    def test_check_verify_code(self):
        _51job.account_init()

        sp = _51job._51Job()
        print(_51job._51_ACCOUNT)
        sp.download_captcha(True, True)
        sp.check_verify_code(input('input verify code:'))