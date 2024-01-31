# -*- encoding: utf-8 -*-
import os
import json
from queue import PriorityQueue
import time
import random
import logging
import threading
import requests
from flask import Flask, jsonify, request

UN_USED_EXPIRED_TIME=2
PER_SIZE_PRODUCER = 10
url = "https://tq.lunaproxy.com/getflowip?neek=1051374&num=10&type=2&sep=1&regions=all&ip_si=1&level=1&sb="

class Proxy:
    def __init__(self, ip, expired_seconds, expired_time):
        self.priority = int(time.time()) + expired_seconds - UN_USED_EXPIRED_TIME * 2
        self.ip = ip
        self.expired_time = expired_time

    def __lt__(self, other):
        return self.priority <= other.priority

    def __gt__(self, other):
        return self.priority > other.priority

    def __str__(self):
        return "Proxy(priority[%s], ip[%s], endtime[%s])" % (self.priority, self.ip, self.expired_time)

    def __eq__(self, other):
        return self.ip == other.ip

class HttpProxyPool:
    def __init__(self):
        self._pressure_ip_proxy_queue = PriorityQueue()
        self._ip_proxies = []
        self._lru_proxies = []
        self._round_robin_index = 0
        self._lock = threading.Lock()

    def put_proxies(self):
        ips = json.loads(requests.get(url % PER_SIZE_PRODUCER).text)["data"]
        print(ips,'xxxxxx')
        for ip in ips:
            host = ip["ip"]
            port = ip["port"]
            expred_seconds = int(ip["timeout"][:ip["timeout"].find("(")])
            expired_time = ip["end_time"]
            proxy = Proxy("%s:%s" % (host, port), expred_seconds, expired_time)

            if not self._exists_proxy(proxy):
                self._put_one_proxy(proxy)
            else:
                logging.info("%s existsed..." % str(proxy))

    def _put_one_proxy(self, proxy):
        try:
            self._lock.acquire()
            self._pressure_ip_proxy_queue.put(proxy)
            self._ip_proxies.append(proxy.ip)
            self._lru_proxies.append(proxy.ip)
        finally:
            self._lock.release()

    def _delete_one_proxy(self, proxy):
        try:
            self._lock.acquire()
            self._ip_proxies.remove(proxy.ip)
            self._lru_proxies.remove(proxy.ip)
        finally:
            self._lock.release()

    def _exists_proxy(self, proxy):
        ip = proxy.ip
        return ip in self._ip_proxies and ip in self._lru_proxies

    def delete_expired_proxies(self):
        while self._pressure_ip_proxy_queue.qsize() > 0:
            proxy = self._pressure_ip_proxy_queue.get()
            priority = proxy.priority
            if priority > int(time.time()):
                self._pressure_ip_proxy_queue.put(proxy)
                break
            else:
                # 少量代理可以使用,大量的时候有性能风险
                self._delete_one_proxy(proxy)
                logging.error("%s expired and removed" % str(proxy))

    def random_get_one_proxy(self):
        return random.choice(self._ip_proxies)

    # random
    def random_get_multi_proxies(self, size):
        if size > len(self._ip_proxies):
            return self._ip_proxies
        return [random.choice(self._ip_proxies) for _ in range(size)]

    # round robin
    def round_robin_get_multi_proxies(self, size):
        results = []
        try:
            self._lock.acquire()
            if size >= len(self._ip_proxies):
                results = self._ip_proxies[:]
                self._round_robin_index = 0
            else:
                if self._round_robin_index >= len(self._ip_proxies):
                    self._round_robin_index = 0
                if self._round_robin_index + size < len(self._ip_proxies):
                    results = self._ip_proxies[self._round_robin_index:self._round_robin_index + size]
                    self._round_robin_index = self._round_robin_index + size
                else:
                    results = self._ip_proxies[self._round_robin_index:] + self._ip_proxies[:self._round_robin_index]
                    self._round_robin_index = size - (len(self._ip_proxies) - self._round_robin_index)
        finally:
            self._lock.release()
        return results

    # lru
    def lru_get_multi_proxies(self, size):
        results = []
        try:
            self._lock.acquire()
            if size >= len(self._lru_proxies):
                results = self._ip_proxies[:]
            else:
                results = self._ip_proxies[:size]
                # 再把前面的放到后面
                for _ in range(size):
                    self._ip_proxies.pop(0)
                self._ip_proxies.extend(results)
        finally:
            self._lock.release()
        return results

    def round_robin_index_(self):
        return self._round_robin_index

    def __len__(self):
        return len(self._ip_proxies)

http_proxy_pool = HttpProxyPool()
# 代理监控
class HttpProxyMonitor(threading.Thread):
    def __init__(self, name):
        super(HttpProxyMonitor, self).__init__(name=name)

    def run(self):
        while True:
            try:
                print("开始监控代理")
                http_proxy_pool.delete_expired_proxies()
                logging.info("current pool size[%s], round_robin_index[%s]" % (len(http_proxy_pool), http_proxy_pool.round_robin_index_()))
                print("current pool size[%s], round_robin_index[%s]" % (len(http_proxy_pool), http_proxy_pool.round_robin_index_()))
                time.sleep(UN_USED_EXPIRED_TIME)
            except:
                pass

# 代理生产者
class HttpProxyProducer(threading.Thread):
    def __init__(self, name):
        super(HttpProxyProducer, self).__init__(name=name)

    def run(self):
        while True:
            try:
                print("开始生产代理")
                http_proxy_pool.put_proxies()
                time.sleep(UN_USED_EXPIRED_TIME * 3)
            except:
                pass

producer = HttpProxyProducer("producer")
monitor = HttpProxyMonitor("monitor")
producer.start()
monitor.start()

app = Flask(__name__)
@app.route('/proxy/random/')
def random_get_proxies():       # http://127.0.0.1:8888/proxy/random/?size=2
    size = int(request.args.get('size'))
    proxies = http_proxy_pool.random_get_multi_proxies(size)
    return jsonify(proxies)

@app.route('/proxy/lru/')
def lru_get_proxies():       # http://127.0.0.1:8888/proxy/lru/?size=2
    size = int(request.args.get('size'))
    proxies = http_proxy_pool.lru_get_multi_proxies(size)
    return jsonify(proxies)

@app.route('/proxy/round_robin/')
def round_robin_get_proxies():       # http://127.0.0.1:8888/proxy/round_robin/?size=2
    size = int(request.args.get('size'))
    proxies = http_proxy_pool.round_robin_get_multi_proxies(size)
    return jsonify(proxies)

# 直接返回requests类型的代理
# from maoyan.common.http_proxy_pool import get_requests_http_ip, get_scrapy_http_ip
def get_requests_http_ip():
    proxy_ip = json.loads(requests.get("http://127.0.0.1:7890/proxy/random/?size=1").text)[1]
    return {"http": "http://%s/" % proxy_ip, "https": "https://%s/" % proxy_ip}

# 直接返回requests类型的代理
def get_scrapy_http_ip(type=0):
    proxy_ip = json.loads(requests.get("http://127.0.0.1:7890/proxy/random/?size=1").text)[1]
    return "%s://%s/" % ("https" if type==0 else "http", proxy_ip)

def init_log_config():
    LOG_FORMAT = "%(asctime)s - %(levelname)s - %(message)s"  # 日志格式化输出
    DATE_FORMAT = "%Y-%m-%d %H:%M:%S %p"  # 日期格式
    if os.name == "posix":
        filename = "/home/libin/maoyan/log/fetch_http_proxy_multiprocessing.log"
    else:
        filename = "d:/fetch_http_proxy_multiprocessing.log"
    fp = logging.FileHandler(filename, encoding='utf-8')
    fs = logging.StreamHandler()
    logging.basicConfig(level=logging.INFO, format=LOG_FORMAT, datefmt=DATE_FORMAT, handlers=[fp, fs])  # 调用

if __name__ == "__main__":
    # init_log_config()
    # app.run(host="127.0.0.1", port=7890)
    print(get_requests_http_ip())


