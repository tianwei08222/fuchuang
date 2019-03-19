# -*- coding: utf-8 -*-

# Scrapy settings for jobspider project
#
# For simplicity, this file contains only settings considered important or
# commonly used. You can find more settings consulting the documentation:
#
#     https://doc.scrapy.org/en/latest/topics/settings.html
#     https://doc.scrapy.org/en/latest/topics/downloader-middleware.html
#     https://doc.scrapy.org/en/latest/topics/spider-middleware.html

BOT_NAME = 'jobspider'

SPIDER_MODULES = ['jobspider.spiders']
NEWSPIDER_MODULE = 'jobspider.spiders'


DUPEFILTER_CLASS = "scrapy_redis.dupefilter.RFPDupeFilter"
# 确保所有的爬虫通过Redis去重
SCHEDULER = "scrapy_redis.scheduler.Scheduler"
# 启用Redis调度存储请求队列
SCHEDULER_PERSIST = True
# 持久化，不清除Redis队列、这样可以暂停/恢复 爬取

REDIS_URL = "redis://127.0.0.1:6379"
# Crawl responsibly by identifying yourself (and your website) on the user-agent
#USER_AGENT = 'jobspider (+http://www.yourdomain.com)'

# Obey robots.txt rules
ROBOTSTXT_OBEY = False


USER_AGENT = 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36'
# Configure maximum concurrent requests performed by Scrapy (default: 16)
#CONCURRENT_REQUESTS = 32

# Configure a delay for requests for the same website (default: 0)
# See https://doc.scrapy.org/en/latest/topics/settings.html#download-delay
# See also autothrottle settings and docs
#DOWNLOAD_DELAY = 3
# The download delay setting will honor only one of:
#CONCURRENT_REQUESTS_PER_DOMAIN = 16
#CONCURRENT_REQUESTS_PER_IP = 16

# Disable cookies (enabled by default)
#COOKIES_ENABLED = False

# Disable Telnet Console (enabled by default)
#TELNETCONSOLE_ENABLED = False

# Override the default request headers:
#DEFAULT_REQUEST_HEADERS = {
#   'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
#   'Accept-Language': 'en',
#}

# Enable or disable spider middlewares
# See https://doc.scrapy.org/en/latest/topics/spider-middleware.html
#SPIDER_MIDDLEWARES = {
#    'jobspider.middlewares.JobspiderSpiderMiddleware': 543,
#}

# Enable or disable downloader middlewares
# See https://doc.scrapy.org/en/latest/topics/downloader-middleware.html

DOWNLOADER_MIDDLEWARES = {
   # 'jobspider.middlewares.ProxyMiddleWare': 100,
   # 'jobspider.middlewares.JobspiderDownloaderMiddleware': 543,
}

# Enable or disable extensions
# See https://doc.scrapy.org/en/latest/topics/extensions.html
#EXTENSIONS = {
#    'scrapy.extensions.telnet.TelnetConsole': None,
#}

# Configure item pipelines
# See https://doc.scrapy.org/en/latest/topics/item-pipeline.html
ITEM_PIPELINES = {
   'scrapy_redis.pipelines.RedisPipeline': 200,
   'jobspider.pipelines.JobspiderPipeline': 300,
}

MYSQL_HOST='127.0.0.1'
MYSQL_USER='root'
MYSQL_PASS='123456'
MYSQL_DB='test'
MYSQL_CHARSET='utf8'