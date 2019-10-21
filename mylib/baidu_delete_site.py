# -*- coding:utf-8 -*-
from requests.exceptions import ConnectionError, ReadTimeout
from json import JSONDecodeError
import time
import requests
import urllib3
urllib3.disable_warnings()


def delete_all_site(site, cookie):
    # 获取现有网站
    site = 'http://' + site + '/'
    fail = 0
    while True:
        headers = {
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8'
                      ',application/signed-exchange;v=b3',
            'Accept-Encoding': 'gzip, deflate, br',
            'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
            'Cache-Control': 'max-age=0',
            'Connection': 'keep-alive',
            'Host': 'ziyuan.baidu.com',
            'Upgrade-Insecure-Requests': '1',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko)'
                          ' Chrome/75.0.3770.142 Safari/537.36',
            'Cookie': cookie
        }
        params = {
            'page': 1,
            'pagesize': 100,
        }
        response = object
        try:
            response = requests.get(
                url='https://ziyuan.baidu.com/site/getsite',
                params=params,
                headers=headers,
                verify=False
            )
            data = response.json()
            print('当前剩余网站：%s  本页数据：%s' % (data['count'], len(data['list'])))

            main_site = site.replace('www.', '')
            fail = 0
            for line in data['list']:
                if line['url'] == site:
                    continue
                if delete_one_site(line['id'], cookie):
                    print(line['id'], line['url'], '删除成功')
                    time.sleep(1)
                else:
                    print(line['id'], line['url'], '删除失败')
                    fail += 1
                    time.sleep(1)
            if fail == 0:
                break
                # if site == line['url'] or main_site == line['url']:
                #     print('查找到 主站：%s 准备删除。。。' % line['url'])
                #     if delete_one_site(line['id'], cookie):
                #         print(line['id'], line['url'], '删除成功')
                #     else:
                #         print(line['id'], line['url'], '删除失败')
        except ConnectionError:
            # print('断开')
            pass
        except JSONDecodeError:
            print(response.content)
            pass


def delete_one_site(site_id, cookie):
    headers = {
        'Host': 'ziyuan.baidu.com',
        'Connection': 'keep-alive',
        'Content-Length': '12',
        'Accept': 'application/json, text/javascript, */*; q=0.01',
        'Origin': 'https://ziyuan.baidu.com',
        'X-Requested-With': 'XMLHttpRequest',
        'X-Request-By': 'baidu.ajax',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko)'
                      ' Chrome/75.0.3770.142 Safari/537.36',
        'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
        'Referer': 'https://ziyuan.baidu.com/site/index',
        'Accept-Encoding': 'gzip, deflate, br',
        'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
        'Cookie': cookie,
    }

    data = 'id=' + site_id
    try:
        response = requests.post(
            url='https://ziyuan.baidu.com/site/delete',
            headers=headers,
            data=data,
            verify=False
        )
        print(response.content)
        data = response.json()
        if site_id in str(data['success']):
            return True
        else:
            return False
    except ConnectionError:
        return False
    except KeyError:
        return False
    except JSONDecodeError:
        return False

