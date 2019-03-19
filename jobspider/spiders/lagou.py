# -*- coding: utf-8 -*-
import scrapy
from scrapy_redis.spiders import RedisSpider

# 拉勾网
class LagouSpider(RedisSpider):
    name = 'lagou'
    allowed_domains = ['lagou.com']
    redis_key = "lagou"

    def parse(self, response):
        pass
