# -*- coding: utf-8 -*-

from scrapy_redis.spiders import RedisSpider
import re
from epubw.keys import *
from epubw.tools import RedisManager, MysqlManager
from epubw.items import BookItem


# 三级页面爬虫
# https://epubw.com/download/?o=47X0QxAcsbWpLI4FDMFHHH8Fu8gaYzAtdxeHO+fRvz8nHWFoUNT4mWIxCnEog8c=
class ForthSpider(RedisSpider):
    name = THIRD_BOOK_SPIDER_NAME
    redis_key = BOOK_THIRD_URL_KEY
    allowed_domains = ['epubw.com']

    def __init__(self):
        self.r = RedisManager().rc
        self.db = MysqlManager()

    def parse(self, response):
        third_url = response.url
        s = response.xpath('//noscript/meta/@content').extract()[0]
        t = re.findall(".*url=\'(.*)\';", s)
        if len(t) == 0:
            print("not find secret {}".format(response.url))
        else:
            item = BookItem()
            item[PAN_URL] = t[0]
            item[THIRD_URL] = third_url
            yield item
