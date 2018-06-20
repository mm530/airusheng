import numpy
from PIL import Image
import random
import requests
from io import BytesIO
import time
import os
import os.path


class TjairCaptcha:

    def download_img(self):
        count = 0
        timeout = 10
        def _download_img(count, timeout):
            count += 1
            if count > 3:
                raise Exception('重试超过3次')
            url = 'https://www.tianjin-air.com/cas/captchaImg?' + str(random.random())
            headers = {
                'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
                'Accept-Encoding':'gzip, deflate, sdch',
                'Accept-Language':'zh-CN,zh;q=0.8',
                'Cache-Control':'max-age=0',
                'Host':'www.tianjin-air.com',
                'Upgrade-Insecure-Requests':'1',
                'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36',
            }
            try:
                r = requests.get(url, headers=headers, stream=True, timeout=timeout)
                r.raise_for_status()
                i = Image.open(BytesIO(r.content))
                if not os.path.exists('tjair_captcha'):
                    os.mkdir('tjair_captcha')
                sf = 'tjair_captcha' + os.path.sep + str(time.time()) + '.jpg'
                i.save(sf)
                print(sf)
            except requests.exceptions.ReadTimeout as e:
                timeout += 5
                _download_img(count, timeout)
            except requests.exceptions.ConnectionError as e:
                _download_img(count, timeout)
        _download_img(count, timeout)

    def split_img(self, img_file):
        if not os.path.exists('tjair_captcha_split'):
            os.mkdir('tjair_captcha_split')
        ima = numpy.array(Image.open(img_file)) # 包含行列颜色通道的图片矩阵
        # ima = numpy.array(Image.open(img_file).convert('L'))  # 灰色图像没有颜色通道
        sp = numpy.shape(ima) # 图片维度(行，列)
        print(sp)
        ima1 = ima[:, 0:20]
        ima2 = ima[:, 20:40]
        ima3 = ima[:, 40:60]
        ima4 = ima[:, 60:80]
        im1 = Image.fromarray(ima1)
        im2 = Image.fromarray(ima2)
        im3 = Image.fromarray(ima3)
        im4 = Image.fromarray(ima4)
        im1.save('tjair_captcha_split' + os.path.sep + str(time.time()) + '.jpg')
        im2.save('tjair_captcha_split' + os.path.sep + str(time.time()) + '.jpg')
        im3.save('tjair_captcha_split' + os.path.sep + str(time.time()) + '.jpg')
        im4.save('tjair_captcha_split' + os.path.sep + str(time.time()) + '.jpg')


def main():
    tc = TjairCaptcha()
    if not os.path.exists(('tjair_captcha')):
        for i in range(100):
            tc.download_img()
    ifs = ['tjair_captcha' + os.path.sep + f for f in os.listdir('tjair_captcha')]
    for imgf in ifs:
        tc.split_img(imgf)


if __name__ == '__main__':
    main()