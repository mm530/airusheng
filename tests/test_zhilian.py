from unittest import TestCase
from airusheng import zhilian


class Test(TestCase):
    def test_login(self):
        zl = zhilian.ZhiLian()
        zl.login()
