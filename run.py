# -*- coding:utf-8 -*-
from mylib.pkg_procedure import send_pkg_url
from threadpool import ThreadPool, makeRequests


pool = ThreadPool(30)
arg = []
success = 0
for thread_num in range(0, 30):
    # arg.append(([thread_num, True, False, 10], None))
    arg.append(thread_num)

request = makeRequests(send_pkg_url, arg)
[pool.putRequest(req) for req in request]
pool.wait()
