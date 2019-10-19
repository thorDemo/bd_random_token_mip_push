# -*-coding:utf-8-*-
import requests
from requests.exceptions import ConnectionError, ReadTimeout
from tools.push_tools import PushTool
import urllib3
from datetime import datetime
urllib3.disable_warnings()


def add_random_site(site, cookie):
    """
    :param site:
    :param cookie:
    :return:
    """

    url = ''
    main_site = str(site).lstrip('www.')
    for x in range(0, 10):
        url = url + 'mipcdn-%s.%s\n' % (PushTool.random_chars(8), main_site)
    site_urls = url.split('\n')
    url = url.strip('\n')
    url = url.replace('\n', '%0A')
    data = 'site=%s&urls=%s' % (site, url)
    # print(data)
    ua = PushTool.user_agent()
    # print(ua)
    headers = {
        'Host': 'ziyuan.baidu.com',
        'Connection': 'keep-alive',
        'Content-Length': str(len(data)),
        'Accept': 'application/json, text/javascript, */*; q=0.0',
        'Origin': 'https://ziyuan.baidu.com',
        'X-Requested-With': 'XMLHttpRequest',
        'X-Request-By': 'baidu.ajax',
        'User-Agent': ua,
        'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
        'Referer': 'https://ziyuan.baidu.com/site/batchadd',
        'Accept-Encoding': 'gzip, deflate, br',
        'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
        'Cookie': cookie
    }
    try:
        # proxy = get_proxy().get("proxy")
        response = requests.post(
            url='https://ziyuan.baidu.com/site/batchaddSubmit',
            headers=headers,
            data=data,
            timeout=30,
            # verify=False,
            # proxies={"http": "http://{}".format(proxy)}
        )
        print(response.status_code, response.content)
        if response.status_code == 200:
            result = response.json()
            try:
                if int(result['status']) == -2:
                    print('添加数量超过上限，请调整后重新提交。', datetime.now().strftime('%a %b %d %H:%M:%S %Y'))
                    return False
                elif int(result['status']) == -1:
                    print('添加数量超过上限，同一主站下可批量添加1000个子站，请调整后重新提交。', datetime.now().strftime('%a %b %d %H:%M:%S %Y'))
                    return False
            except KeyError:
                pass
            for line in result['errList']:
                if int(line['status']) == 4:
                    print('添加网站--', line['url'], '--重复', datetime.now().strftime('%a %b %d %H:%M:%S %Y'))
                elif int(line['status']) == 2:
                    print('添加网站--', line['url'], '--DNS解析失败，网站不存在', datetime.now().strftime('%a %b %d %H:%M:%S %Y'))
                elif int(line['status']) == 0:
                    print('添加网站--', line['url'], '--成功', datetime.now().strftime('%a %b %d %H:%M:%S %Y'))
                elif int(line['status']) == -2:
                    print('添加网站--', line['url'], '--添加数量超过上限', datetime.now().strftime('%a %b %d %H:%M:%S %Y'))
                else:
                    print('添加网站--', line['url'], '--异常', datetime.now().strftime('%a %b %d %H:%M:%S %Y'))
            return site_urls
        else:
            return None
    except ConnectionError:
        # print('服务器断开连接。。。')
        return None
    except ReadTimeout:
        # print('服务器连接超时。。。')
        return None

#
# def get_proxy():
#     return requests.get("http://127.0.0.1:5010/get/").json()

