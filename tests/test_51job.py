from unittest import TestCase
from airusheng import _51job
import urllib.parse
import os

import logging
logging.basicConfig(level=logging.DEBUG)

class Test(TestCase):
    def test_local_test(self):
        _51job.local_test()

    def test_distribute_delivery(self):
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

    def test_local_many_test(self):
        os.environ['http_proxy'] = '180.121.129.74:808'
        _51job.local_many_test()