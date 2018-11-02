import random
# 导入官方文档对应的HttpProxyMiddleware
from scrapy.contrib.downloadermiddleware.httpproxy import HttpProxyMiddleware
import redis
class IPPOOLS(HttpProxyMiddleware):
    def __init__(self,ip=''):
        self.ip = ip

    def process_request(self, request, spider):
        # 随机选择一个代理ip
        thisip = random.choice(self.read_ippools())
        print("当前的代理ip为:",thisip)
        request.meta["proxy"] = thisip

    # 定义一个辅助函数，用于读取代理池
    def read_ippools(self):
        r = redis.StrictRedis(host='192.168.10.131', port=6379, db=0, charset='utf-8')
        ip_list = r.lrange('ip', 0, 30)
        return ip_list
