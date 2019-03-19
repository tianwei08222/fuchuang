# -*- coding: utf-8 -*-
import scrapy
from scrapy_redis.spiders import RedisSpider

# 智联招聘
class ZhaopinSpider(RedisSpider):
    name = 'zhaopin'
    allowed_domains = ['zhaopin.com']
    redis_key = "zhaopin"

    def parse(self, response):
        pass
