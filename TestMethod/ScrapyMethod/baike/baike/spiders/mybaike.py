import scrapy
from scrapy.spiders import Rule
from scrapy_redis.spiders import RedisSpider
class MybaikeSpider(RedisSpider):
    name = 'mybaike'
    allowed_domains = ['baidu.com']
    start_urls = ['http://baidu.com/']

    def parse(self, response):
        print('我是一个兵大头兵')
        # pass
