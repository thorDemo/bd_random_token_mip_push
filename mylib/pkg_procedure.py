from tools.push_tools import PushTool
import requests
from requests.exceptions import ConnectionError, ChunkedEncodingError
from datetime import datetime
from random import choice, randint
from json.decoder import JSONDecodeError

# all_site = PushTool.get_all_site()


def send_pkg_url(domain):
    # pre_num = 6
    # while pre_num:
        # static = 'mipcdn1693.aienao.com'
    url = ''
        # if pre_num == 6:
        #     for x in range(0, 100):
        #         url += PushTool.rand_all(domain) + '\n'
        #     url = url.strip('\n')
        # elif pre_num == 1:
        #     for x in range(0, 1900):
        #         url += PushTool.rand_all(domain) + '\n'
        #     url = url.strip('\n')
        # else:
        #     for x in range(0, 2000):
        #         url += PushTool.rand_all(domain) + '\n'
        #     url = url.strip('\n')
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
    response = object
    try:
        response = requests.post(target_url, data=url, headers=headers)
        message = response.json()['message']
        print(datetime.now(), domain, response.json())
        return message
    except ConnectionError:
        # print(datetime.now(), 'pkg_procedure\t服务器断开连接。。。')
        pass
    except ChunkedEncodingError:
        # print(datetime.now(), 'pkg_procedure\t远程主机强迫关闭了一个现有的连接。。。')
        pass
    except JSONDecodeError:
        # print(datetime.now(), 'pkg_procedure\t服务器未返回正确数据。。')
        pass
    except KeyError:
        message = response.json()
        print(datetime.now(), domain, message)

