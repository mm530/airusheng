import requests
from lxml import etree
import os
import os.path


class IP:
    def __init__(self, ip, port, type, speed, check_time):
        self.ip = ip
        self.port = port
        self.type = type
        self.speed = speed
        self.check_time = check_time


class Kuaidaili_com:
    free_inha_count = 0
    free_inha_timeout = 5
    def free_inha(self, page=1):
        url = 'https://www.kuaidaili.com/free/inha/%d/' % page
        try:
            r = requests.get(url, headers={
                'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
                'Accept-Encoding':'gzip, deflate, br',
                'Accept-Language':'zh-CN,zh;q=0.9',
                'Cache-Control':'max-age=0',
                'Host': 'www.kuaidaili.com',
                'Upgrade-Insecure-Requests':'1',
                'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36',
            }, timeout=self.free_inha_timeout)
        except requests.exceptions.ReadTimeout as e:
            self.free_inha_timeout += 5
            self.free_inha(page)
        except requests.exceptions.ConnectionError as e:
            raise Exception('快代理访问国内高匿代理分页时，服务器丢弃了这个请求')
        else:
            r.raise_for_status()
            r.encoding = 'utf-8'
            ips = []
            try:
                page = etree.HTML(r.text)
                trs = page.xpath('//table[@class="table table-bordered table-striped"]/tbody/tr')
                for tr in trs:
                    tds = tr.xpath('./td')

                    ip = tds[0].xpath('./text()')[0].strip()
                    port = tds[1].xpath('./text()')[0].strip()
                    type = tds[3].xpath('./text()')[0].strip().lower()
                    speed = tds[5].xpath('./text()')[0].strip()[:-1]
                    check_time = tds[6].xpath('./text()')[0].strip()

                    ips.append(IP(ip, port, type, speed, check_time))
            except Exception as e:
                print(e)
                if not os.path.exists('kuaidaili_com'):
                    os.mkdir('kuaidaili_com')
                else:
                    with open('kuaidaili_com' + os.path.sep + url + '.err') as f:
                        f.write(r.text)
            return ips


class Ip_seofangfa_com:
    def index(self):
        url = 'https://ip.seofangfa.com/'
        headers = {

        }
        r = requests.get(url, headers=headers)
        r.raise_for_status()
        r.encoding = 'utf-8'
        page = etree.HTML(r.text)
        trs = page.xpath('//table[@class="table"]/tbody/tr')
