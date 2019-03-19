import scrapy.cmdline
import redis

def main():
    rds = redis.Redis(host='127.0.0.1', port=6379, db=0)
    redis_key = 'qcwy'
    rds.flushdb()
    url_list = ['https://search.51job.com/list/000000,000000,0000,00,9,99,Java,2,1.html',
                'https://search.51job.com/list/000000,000000,0000,00,9,99,Python,2,1.html',
                'https://search.51job.com/list/000000,000000,0000,00,9,99,%25E5%2589%258D%25E7%25AB%25AF,2,1.html',
                'https://search.51job.com/list/000000,000000,0000,00,9,99,%25E5%25A4%25A7%25E6%2595%25B0%25E6%258D%25AE,2,1.html',
                'https://search.51job.com/list/000000,000000,0000,00,9,99,%25E4%25BA%25BA%25E5%25B7%25A5%25E6%2599%25BA%25E8%2583%25BD,2,1.html',
                'https://search.51job.com/list/000000,000000,0000,00,9,99,%25E8%25BD%25AF%25E4%25BB%25B6%25E6%25B5%258B%25E8%25AF%2595,2,1.html',
                'https://search.51job.com/list/000000,000000,0000,00,9,99,%25E5%2585%25A8%25E6%25A0%2588%25E5%25B7%25A5%25E7%25A8%258B%25E5%25B8%2588,2,1.html',
                'https://search.51job.com/list/000000,000000,0000,00,9,99,C%252FC%252B%252B,2,1.html',
                'https://search.51job.com/list/000000,000000,0000,00,9,99,%25E4%25BA%25A7%25E5%2593%2581%25E7%25BB%258F%25E7%2590%2586,2,1.html'
                ]
    for url in url_list:
        rds.lpush(redis_key, url)
    scrapy.cmdline.execute(['scrapy','crawl','qcwy'])

if __name__ == '__main__':
    main()

# import os
# import sys
# print(os.getcwd())
# os.chdir("E://Python项目//jobspider//jobspider")
# print(os.getcwd())