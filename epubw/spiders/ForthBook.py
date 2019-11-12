# -*- coding: utf-8 -*-

from scrapy_redis.spiders import RedisSpider
import re
from epubw.keys import *
from epubw.tools import RedisManager, MysqlManager


class ForthSpider(RedisSpider):
    # https://epubw.com/download/?o=47X0QxAcsbWpLI4FDMFHHH8Fu8gaYzAtdxeHO+fRvz8nHWFoUNT4mWIxCnEog8c=
    name = 'ForthBook'
    redis_key = BOOK_FORTH_URL_KEY
    allowed_domains = ['epubw.com']

    def __init__(self):
        self.r = RedisManager().rc
        self.db = MysqlManager()

    def parse(self, response):
        s = response.xpath('//noscript/meta/@content').extract()[0]
        t = re.findall(".*url=\'(.*)\';", s)
        if len(t) == 0:
            print(response.url)
        else:
            id = self.r.hget(BOOK_THIRD_ID_HASH, response.url)
            sql = 'update book set pan_url=%s where id=%s'
            self.db.execute_dml(sql, t[0], int(id))
            print("{}:{}".format(id, t[0]))
