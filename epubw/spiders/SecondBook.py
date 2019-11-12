# -*- coding: utf-8 -*-
import re

from scrapy_redis.spiders import RedisSpider

from epubw.keys import *
from epubw.tools import RedisManager, MysqlManager


class SecondSpider(RedisSpider):
    name = 'SecondBook'
    redis_key = BOOK_SECOND_URL_KEY
    allowed_domains = ['epubw.com']

    def __init__(self):
        self.r = RedisManager().rc
        self.db = MysqlManager()

    def parse(self, response):
        url = response.url
        link = response.xpath('//div[@class="list"]/a/@href').extract()[0]
        name = response.xpath('//div[@class="desc"]/p/text()').extract()[0]
        name = re.findall('文件名称：《(.*)》', name)[0]
        id = self.r.hget(BOOK_ID_HASH, url)
        print(id)
        if id is None:
            print("{} not exists".format(id))
            return
        sql = 'update book set name=%s,url=%s where id=%s'
        self.db.execute_dml(sql, name, url, int(id))

    # def closed(self, reason):
    #     for s in self.last_book_set:
    #         self.f.write(s + "\n")
    #     print("crawl over, save file")
    #     self.f.close()
