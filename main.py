import queue
import random
import re
import time

import requests
from bs4 import BeautifulSoup


class DownPic:

    def __init__(self):
        self.headers = {
            'Accept': 'text/html,application/xhtml+xml,application/xml;q =0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3',
            'Accept-Encoding': 'gzip,deflate',
            'Accept-Language': 'zh-CN,zh;q=0.9',
            'Cache-Control': 'max-age=0',
            'Connection': 'keep-alive',
            'Host': 'desk.zol.com.cn',
            'User-Agent': 'Mozilla/5.0(Macintosh;Intel Mac OS X 10_13_3) AppleWebKit/537.36(KHTML, like Gecko) Chrome/76.0.3809.100 Safari/537.36'
        }

        self.lists_queue = queue.Queue()
        self.down_queue = queue.Queue()

        self.down_path = '/Users/baymax/Pictures/pics/'

        self.main_url = 'http://desk.zol.com.cn'

        self.type_lists = [
            'http://desk.zol.com.cn/meinv/',
            'http://desk.zol.com.cn/chemo/',
        ]

    def get_html(self, url):
        r = requests.get(url=url, headers=self.headers)
        soup = BeautifulSoup(r.text, 'lxml')
        return soup

    def get_lists(self):
        for i in self.type_lists:
            soup = self.get_html(i)
            lists = soup.select('li.photo-list-padding > a.pic')
            for j in lists:
                url = self.main_url + j.get('href')
                # print(url)
                self.lists_queue.put(url)

    def get_suite(self):
        while not self.lists_queue.empty():
            i = self.lists_queue.get()
            soup = self.get_html(i)
            suites = soup.find_all({'img': True})
            for j in suites[8:-12]:
                x = j.get('src') or j.get('srcs')
                print(x)
                self.down_queue.put(x)
            print('end loop')
            time.sleep(random.randint(1, 5))
        print('end')

    def download(self):
        headers = {
            'Accept': 'text/html,application/xhtml+xml,application/xml;q =0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3',
            'accept-encoding': 'gzip, deflate, br',
            'accept-language': 'zh-CN,zh;q=0.9',
            'cache-control': 'max-age=0',
            'sec-fetch-mode': 'navigate',
            'sec-fetch-site': 'none',
            'sec-fetch-user': '?1',
            'upgrade-insecure-requests': '1',
            'User-Agent': 'Mozilla/5.0(Macintosh;Intel Mac OS X 10_13_3) AppleWebKit/537.36(KHTML, like Gecko) Chrome/76.0.3809.100 Safari/537.36'
        }
        while not self.down_queue.empty():
            i = self.down_queue.get()
            i = re.sub('144x90', '1860x1050', i)
            r = requests.get(url=i, headers=headers)
            name = i.split('/')[-1]
            print('downloading\t{}'.format(i))
            with open(self.down_path + name, 'wb') as f:
                f.write(r.content)
            print('downloaded')
            time.sleep(random.randint(1, 5))


if __name__ == '__main__':
    a = DownPic()
    a.get_lists()
    a.get_suite()
    a.download()
