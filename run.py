# -*- coding:utf-8 -*-
from mylib.pkg_procedure import send_pkg_url
from mylib.baidu_add_site import add_random_site
from mylib.baidu_delete_site import delete_all_site
from configparser import ConfigParser
from threadpool import ThreadPool, makeRequests


# pool = ThreadPool(4)
# arg = []
# success = 0
# for fan in range(1330, 2000):
#     # arg.append(([thread_num, True, False, 10], None))
#     arg.append('mipcdn%s.aienao.com' % fan)
#
# request = makeRequests(send_pkg_url, arg)
# [pool.putRequest(req) for req in request]
# pool.wait()
cookie_file = open('cookies.txt', 'r', encoding='utf-8')
cookie = cookie_file.readline().strip()
config = ConfigParser()
config.read('push_config.ini', 'utf-8')
domain = config.get('bd_push', 'domain')
while True:
    # 添加10个网站
    site_urls = None
    while site_urls is None:
        site_urls = add_random_site(site=domain, cookie=cookie)
    # 全额推送
    for urls in site_urls:
        send_pkg_url(domain=urls)
    # 删除网站
    delete_all_site(site=domain, cookie=cookie)

