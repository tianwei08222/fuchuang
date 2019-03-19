# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import pymysql.cursors
import jieba
from pykafka import KafkaClient

class JobspiderPipeline(object):
    able_word_set = set()
    tech_word_set = set()
    def __init__(self):
        able_word_list = []
        tech_word_list = []
        with open('ability.txt', 'r',encoding='gbk') as f:
            for i in f:
                able_word_list = list(i.split(','))
        for i in able_word_list:
            self.able_word_set.add(i)
        with open('technology.txt', 'r') as f:
            for i in f:
                tech_word_list = list(i.split(','))
        for i in tech_word_list:
            self.tech_word_set.add(i)

    # 能力和技术关键词分词结果集
    able_word = set()
    tech_word = set()
    def cut(self,str):
        self.able_word = set()
        self.tech_word = set()
        key_word_list = jieba.cut(str)
        for i in key_word_list:
            if i in self.able_word_set:
                self.able_word.add(i)
            elif i in self.tech_word_set:
                self.tech_word.add(i)

    connect = pymysql.Connect(
        host='localhost',
        port=3306,
        user='root',
        passwd='123456',
        db='job',
        charset='utf8'
    )
    # 获取游标
    cursor = connect.cursor()
    #  数据插入mysql
    def process_item(self, item, spider):
        sql = "INSERT INTO software_enginee_two (direction_id, job_name,company_name,job_site,job_salary,relase_date,job_info1,company_welfare,job_info2,company_type,company_people_num,company_business) VALUES (%d,'%s', '%s','%s','%s','%s','%s','%s','%s','%s','%s','%s' )"

        dir = 1
        if (item['dir'] == '大数据') : dir = 1
        elif (item['dir'] == '人工智能'): dir = 2
        elif (item['dir'] == '产品经理'): dir = 3
        elif (item['dir'] == '全栈工程师'): dir = 4
        elif (item['dir'] == 'C/C++'): dir = 5
        elif (item['dir'] == '软件测试'): dir = 6
        elif (item['dir'] == '前端'): dir = 7
        elif (item['dir'] == 'Java'): dir = 8
        elif (item['dir'] == 'Python'): dir = 9
        data = (dir,item['job_name'],item['company'],item['place'],item['salary'],item['time'],item['job_info'],item['benefits'],item['job_detail'],item['company_type'],item['company_people_num'],item['company_business'])
        # self.cut(item['job_detail'])
        # print(','.join(self.able_word))
        # print(','.join(self.tech_word))
        # item['able']=','.join(self.able_word)
        # item['tech']=','.join(self.tech_word)
        # sql = "INSERT INTO software_enginee (direction_id, job_name,company_name,job_site,job_salary,relase_date,job_info1,company_welfare,job_info2,company_type,company_people_num,company_business,able,tech) VALUES (%d,'%s', '%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s' )"
        # data = (dir, item['job_name'], item['company'], item['place'], item['salary'], item['time'], item['job_info'],item['benefits'], item['job_detail'], item['company_type'], item['company_people_num'],item['company_business'],item['able'],item['tech'])
        self.cursor.execute(sql % data)
        self.connect.commit()
        return item

    def close_spider(self, spider):
        self.cursor.close()
        self.connect.close()