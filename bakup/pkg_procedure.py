from tools.push_tools import PushTool
import requests
from urllib import parse
from datetime import datetime
from random import choice, randint

success_num = 0
failure_num = 0
cookie = PushTool.get_cookies()
start_time = datetime.now()
all_site = PushTool.get_all_site()


def send_pkg_url(thread_num, is_cookie, is_proxy, timeout):
    domain = 'mip-cache-%s.' % randint(1000, 2000) + choice(all_site)
    while True:
        code = 404
        proxy = ''
        global success_num
        global failure_num
        global start_time
        target = PushTool.rand_all(domain)
        before = PushTool.rand_all(domain)
        headers = {
            'User-Agent': PushTool.user_agent(),
            'Referer': target,
            'Accept': '*/*',
            'Accept-Encoding': 'gzip, deflate',
            'Accept-Language': 'zh-CN,zh;q=0.8',
            'Connection': 'keep-alive',
            'Host': 'api.share.baidu.com',
        }
        payload = {
            'l': target,
            'r': before
        }
        try:
            if is_cookie and is_proxy:
                proxy = PushTool.get_proxy().get("proxy")
                if isinstance(proxy, bytes):
                    proxy = proxy.decode('utf8')
                proxies = {"http": "http://{}".format(proxy)}
                conn = requests.Session()
                conn.headers = headers
                cookies_jar = requests.utils.cookiejar_from_dict(cookie, cookiejar=None, overwrite=True)
                conn.cookies = cookies_jar
                res = conn.get('http://api.share.baidu.com/s.gif', params=payload, timeout=timeout, proxies=proxies)

            elif is_cookie and is_proxy is False:
                conn = requests.Session()
                conn.headers = headers
                cookies_jar = requests.utils.cookiejar_from_dict(cookie, cookiejar=None, overwrite=True)
                conn.cookies = cookies_jar
                res = conn.get('http://api.share.baidu.com/s.gif', params=payload, timeout=timeout)

            elif is_cookie is False and is_proxy:
                proxy = PushTool.get_proxy().get("proxy")
                if isinstance(proxy, bytes):
                    proxy = proxy.decode('utf8')
                proxies = {"http": "http://{}".format(proxy)}
                res = requests.get(
                    'http://api.share.baidu.com/s.gif',
                    params=payload,
                    headers=headers,
                    proxies=proxies,
                    timeout=timeout,
                )
            else:
                res = requests.get(
                    'http://api.share.baidu.com/s.gif',
                    params=payload,
                    headers=headers,
                    timeout=timeout,
                )
            code = res.status_code
            url = parse.unquote(res.url)
            if code == 200:
                if url == 'http://www.baidu.com/search/error.html':
                    failure_num += 1
                else:
                    success_num += 1
            else:
                failure_num += 1

        except Exception as e:
            print(e)
            failure_num += 1

        this_time = datetime.now()
        spend = this_time - start_time
        if int(spend.seconds) == 0:
            speed_sec = success_num / 1
        else:
            speed_sec = success_num / int(spend.seconds)
        speed_day = float('%.2f' % ((speed_sec * 60 * 60 * 24) / 10000000))
        if code == 200:
            print('\033[034m thread_num:{}\tstatus:{}\tproxy：{}\tspeed:{}\tsite_url:{:<20}\t'.format(
                thread_num,
                code,
                is_proxy,
                speed_day,
                target,
            ))
        else:
            print('\033[031m thread_num:{}\tstatus:{}\tproxy：{}\tspeed:{}\tsite_url:{:<20}\t'.format(
                thread_num,
                code,
                is_proxy,
                speed_day,
                target,
            ))



