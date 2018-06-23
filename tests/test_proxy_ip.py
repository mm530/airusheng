from unittest import TestCase
from airusheng.proxy_ip import Kuaidaili_com
import time


class Test(TestCase):
    def test_free_inha(self):
        kc = Kuaidaili_com()
        for i in range(3):
            ips = kc.free_inha(i + 1)
            for ip in ips:
                print(ip.ip, ip.port, ip.type, ip.speed, ip.check_time)
            time.sleep(10)