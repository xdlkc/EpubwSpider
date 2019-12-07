# -*- coding: utf-8 -*-
import time

from scrapy_redis.spiders import RedisSpider
from epubw.items import BookItem
from epubw.keys import *
from epubw.tools import RedisManager, MysqlManager


# 一级页面爬虫：https://epubw.com/326502.html
class FirstBookSpider(RedisSpider):
    name = FIRST_BOOK_SPIDER_NAME
    redis_key = BOOK_FIRST_URL_KEY
    allowed_domains = ['epubw.com']
    # 默认填充内容
    unknown_name = 'unknown'

    def __init__(self):
        self.r = RedisManager().rc
        self.db = MysqlManager()

    def parse(self, response):
        first_url = response.url
        second_url = response.xpath('//table[@class="dltable"]/tbody/tr[last()]/td/a/@href').extract()[0]
        info_dom = response.xpath('//div[@class="bookinfo"]/ul/li')

        # 作者信息
        author = info_dom[1].xpath('./a/text()').extract()
        if len(author) > 0:
            author = author[0]
        else:
            author = info_dom[1].xpath('./text()').extract()
            if len(author) > 0:
                author = author[0]
            else:
                author = self.unknown_name

        # 出版日期
        d = info_dom[2].xpath('./a').xpath('string()').extract()
        if len(d) > 0:
            d = d[0]
        else:
            d = ''
        date = info_dom[2].xpath('./text()').extract()
        if len(date) > 0:
            date = '{}{}'.format(d, date[0])
            ts = time.strptime(date, "%Y-%m")
            date = time.strftime("%Y/%m/%d %H:%M:%S", ts)
        else:
            date = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())

        # 出版社
        publisher = info_dom[3].xpath('./a/text()').extract()
        if len(publisher) > 0:
            publisher = publisher[0]
        else:
            publisher = self.unknown_name

        # isbn号
        isbn = info_dom[5].xpath('./text()').extract()
        if len(isbn) > 0:
            isbn = isbn[0]
        else:
            isbn = self.unknown_name

        item = BookItem()
        item[AUTHOR] = author
        item[PUBLISH_DATE] = date
        item[PUBLISHER] = publisher
        item[ISBN] = isbn
        item[SECOND_URL] = second_url
        item[FIRST_URL] = first_url
        yield item
