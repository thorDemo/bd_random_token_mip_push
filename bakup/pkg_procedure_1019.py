from tools.push_tools import PushTool
import requests
from requests.exceptions import ConnectionError
from datetime import datetime
from random import choice, randint
from json.decoder import JSONDecodeError

all_site = PushTool.get_all_site()


def send_pkg_url(thread_num):
    while True:
        domain = 'mip-cache-%s.' % PushTool.random_chars(8) + choice(all_site)
        # static = 'mip-cache-%s.' % randint(1000, 2000) + 'aienao.com'
        # static = 'www.' + choice(all_site)
        # static = 'www1.' + 'aienao.com'
        url = ''
        for x in range(0, 100):
            url += PushTool.rand_all(domain) + '\n'
        url = url.strip('\n')
        headers = {
            'User-Agent': 'curl/7.12.1',
            'Host': 'data.zz.baidu.com',
            'Content-Type': 'text/plain',
            'Content-Length': str(len(url)),
        }
        target_url = 'http://data.zz.baidu.com/urls?site=%s&token=F5KnjXlVWrKS3MFm&type=mip' % domain
        try:
            requests.post(target_url, data=url, headers=headers)
            response = requests.post(target_url, data=url, headers=headers)
            print(datetime.now(), response.json(), domain)

        except ConnectionError:
            print('服务器断开连接。。。')
        except JSONDecodeError:
            print('服务器未返回正确数据。。')