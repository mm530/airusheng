from unittest import TestCase
from airusheng import _51job


class Test(TestCase):
    def test_local_test(self):
        _51job.local_test()

    def test_distribute_delivery(self):
        _51job.distribute_delivery()

    def test_do_delivery_task(self):
        _51job.do_delivery_task()

    def test_check_i_51job_com(self):
        _51job.check_i_51job_com()