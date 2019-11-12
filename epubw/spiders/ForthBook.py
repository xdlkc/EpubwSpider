# -*- coding: utf-8 -*-

from scrapy_redis.spiders import RedisSpider

from epubw.keys import *
from epubw.tools import RedisManager, MysqlManager


class ThirdSpider(RedisSpider):
    name = 'ThirdBook'
    redis_key = BOOK_THIRD_URL_KEY
    allowed_domains = ['epubw.com']

    def __init__(self):
        self.r = RedisManager().rc
        self.db = MysqlManager()

    def parse(self, response):
        url = response.url
        s = response.xpath('//div[@class="list"]/a/@href').extract()[0]
        id = self.r.hget(BOOK_LAST_ID_HASH, url)
        print(id)
        if id is None:
            print("{} not exists".format(id))
            return
        sql = 'update book set last_url=%s where id=%s'
        self.db.execute_dml(sql, s, int(id))

    # def closed(self, reason):
    #     for s in self.last_book_set:
    #         self.f.write(s + "\n")
    #     print("crawl over, save file")
    #     self.f.close()
