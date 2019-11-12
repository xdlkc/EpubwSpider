# -*- coding: utf-8 -*-

from scrapy_redis.spiders import RedisSpider
import re
from epubw.keys import *
from epubw.tools import RedisManager, MysqlManager


class ThirdSpider(RedisSpider):
    name = 'ThirdBook'
    redis_key = BOOK_THIRD_URL_KEY
    allowed_domains = ['epubw.com']
    # https://epubw.com/download/?o=vfO5Cg==

    def __init__(self):
        self.r = RedisManager().rc
        self.db = MysqlManager()

    def parse(self, response):
        parent_url = response.url
        link = response.xpath('//div[@class="list"]/a/@href').extract()[0]
        secret = response.xpath('//div[@class="desc"]/p/text()')[-1].extract()
        code = re.findall('.*百度网盘密码：(.*)', secret)[0].strip()
        id = self.r.hget(BOOK_LAST_ID_HASH, parent_url)
        if id is None:
            print("{} not exists".format(id))
            return
        # sql = 'update book set last_url=%s where id=%s'
        sql = 'update book set secret = %s where id =%s '
        self.db.execute_dml(sql, code, int(id))
