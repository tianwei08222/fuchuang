# -*- coding: utf-8 -*-
import scrapy
from scrapy_redis.spiders import RedisSpider
import re
import datetime

class QcwyspiderSpider(RedisSpider):
    name = 'qcwy'
    allowed_domains = ['51job.com']
    # urls_list=['python']
    # for i in urls_list:
    # start_urls = ['https://search.51job.com/list/000000,000000,0000,00,9,99,Python,2,1.html']
    redis_key = "qcwy"

    def parse(self, response):
        # 职业方向
        dir = response.xpath("//p[@class='ipt']/input/@value").extract_first()
        div_list = response.xpath("//div[@id='resultList']/div[@class='el']")
        for div in div_list:
            item = dict()
            item['dir'] = dir
            # 职位名
            item['job_name'] = div.xpath("./p/span/a/@title").extract_first()
            # 公司名
            item['company'] = div.xpath("./span/a/@title").extract_first()
            # 工作地点
            item['place'] = div.xpath("./span[@class='t3']/text()").extract_first()
            # 薪资
            item['salary'] = div.xpath("./span[@class='t4']/text()").extract_first()
            # 发布时间
            item['time'] = div.xpath("./span[@class='t5']/text()").extract_first()

            # 只爬取当天的信息
            time = item['time']
            if time is not None:
                today = str(datetime.datetime.now().month) + "-"
                if datetime.datetime.now().month < 10:
                    today = "0" + today
                if datetime.datetime.now().day < 10:
                    today = today + "0"
                today = today + str(datetime.datetime.now().day)
                if (time == today):
                    href = div.xpath("./p/span/a/@href").extract_first()
                    yield scrapy.Request(
                        href,
                        callback=self.parse_job_info,
                        meta={"item": item}
                    )

        next_url = response.xpath("//div[@class='dw_page']//ul/li")[-1]
        next_url = next_url.xpath("./a/@href").extract_first() if len(next_url.xpath("./a/@href")) > 0 else None

        if next_url is not None:
            yield scrapy.Request(
                next_url,
                callback=self.parse
                #meta={"item": item}
             )

    # 爬取职位和公司详情
    def parse_job_info(self, response):
        item = response.meta["item"]
        #岗位信息 job_info
        job_info = response.xpath("//p[@class='msg ltype']/text()").extract()
        job_info = [re.sub(r"\xa0|\t|\s", "", i) for i in job_info]
        job_info = ','.join(job_info)
        item['job_info'] = job_info

        # 公司福利 benefits
        benefits = response.xpath("//div[@class='t1']/span[@class='sp4']/text()").extract()
        benefits = [re.sub(r"\xa0|\t|\s", "", i) for i in benefits]
        benefits = ','.join(benefits)
        item['benefits'] = benefits

        # （具体）职位信息 job_detail
        job_detail = response.xpath("//div[@class='bmsg job_msg inbox']/p/text()").extract()
        job_detail = [re.sub(r"\xa0|\t|\s", "", i) for i in job_detail]
        job_detail = ','.join(job_detail)
        item['job_detail'] = job_detail

        # 公司类型	公司人数 公司业务
        # company_type company_people_num company_business
        length = len(response.xpath("//div[@class='com_tag']/p/@title"))
        item['company_type'] = None
        item['company_people_num'] = None
        item['company_business'] = None
        if( length >= 1 ) :
            item['company_type'] = response.xpath("//div[@class='com_tag']/p/@title").extract()[0]
        if( length >= 2 ) :
            item['company_people_num'] = response.xpath("//div[@class='com_tag']/p/@title").extract()[1]
        if( length >= 3 ) :
            item['company_business'] = response.xpath("//div[@class='com_tag']/p/@title").extract()[2]

        yield item

# Java、Python、前端、大数据、人工智能、软件测试、全栈工程师、C/C++、产品经理
# lpush qcwy https://search.51job.com/list/000000,000000,0000,00,9,99,Java,2,1.html
# lpush qcwy https://search.51job.com/list/000000,000000,0000,00,9,99,Python,2,1.html
# lpush qcwy https://search.51job.com/list/000000,000000,0000,00,9,99,%25E5%2589%258D%25E7%25AB%25AF,2,1.html
# lpush qcwy https://search.51job.com/list/000000,000000,0000,00,9,99,%25E5%25A4%25A7%25E6%2595%25B0%25E6%258D%25AE,2,1.html
# lpush qcwy https://search.51job.com/list/000000,000000,0000,00,9,99,%25E4%25BA%25BA%25E5%25B7%25A5%25E6%2599%25BA%25E8%2583%25BD,2,1.html
# lpush qcwy https://search.51job.com/list/000000,000000,0000,00,9,99,%25E8%25BD%25AF%25E4%25BB%25B6%25E6%25B5%258B%25E8%25AF%2595,2,1.html
# lpush qcwy https://search.51job.com/list/000000,000000,0000,00,9,99,%25E5%2585%25A8%25E6%25A0%2588%25E5%25B7%25A5%25E7%25A8%258B%25E5%25B8%2588,2,1.html
# lpush qcwy https://search.51job.com/list/000000,000000,0000,00,9,99,C%252FC%252B%252B,2,1.html
# lpush qcwy https://search.51job.com/list/000000,000000,0000,00,9,99,%25E4%25BA%25A7%25E5%2593%2581%25E7%25BB%258F%25E7%2590%2586,2,1.html


# 统计每个方向下的职位数
# select direction_id,count(id) from software_enginee group by direction_id;


# wget http://mirrors.hust.edu.cn/apache/kafka/2.1.1/kafka_2.11-2.1.1.tgz
# sudo tar -xzf kafka_2.11-2.1.1.tgz -C /opt/
# sudo wget jdk-8u201-linux-x64.tar.gz

# export JAVA_HOME=/usr/java/jdk1.8.0_201
# export JRE_HOME=/usr/java/jdk1.8.0_201/jre
# export CLASSPATH=.:$JAVA_HOME/lib:$JRE_HOME/lib:$CLASSPATH
# export PATH=$JAVA_HOME/bin:$JRE_HOME/bin:$PATH