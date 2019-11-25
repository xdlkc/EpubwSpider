# -*- coding: utf-8 -*-
import re

from scrapy_redis.spiders import RedisSpider
from epubw.keys import *
from epubw.tools import RedisManager, MysqlManager
from epubw.items import BookItem


# 二级页面爬虫：https://epubw.com/download/?o=ufa4A1U=
class SecondSpider(RedisSpider):
    name = SECOND_BOOK_SPIDER_NAME
    redis_key = BOOK_SECOND_URL_KEY
    allowed_domains = ['epubw.com']

    def __init__(self):
        self.r = RedisManager().rc
        self.db = MysqlManager()

    def parse(self, response):
        second_url = response.url
        third_url = response.xpath('//div[@class="list"]/a/@href').extract()[0]
        # name = response.xpath('//div[@class="desc"]/p/text()').extract()[0]
        # name = re.findall('文件名称：《(.*)》', name)[0]
        secret = response.xpath('//div[@class="desc"]/p/text()')[-1].extract()
        # 网盘提取密码
        code = re.findall('.*百度网盘密码：(.*)', secret)[0].strip()
        # 推送至redis队列
        self.r.lpush(BOOK_THIRD_URL_KEY, third_url)
        item = BookItem()
        item[SECOND_URL] = second_url
        item[THIRD_URL] = third_url
        item[SECRET] = code
        yield item
