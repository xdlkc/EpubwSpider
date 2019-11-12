# -*- coding: utf-8 -*-
import time
from scrapy_redis.spiders import RedisSpider
from epubw.tools import RedisManager
from epubw.items import BookItem
from epubw.keys import *


class BookSpider(RedisSpider):
    name = 'Book'
    redis_key = BOOK_FIRST_URL_KEY
    over_key = OVER_BOOK_KEY
    allowed_domains = ['epubw.com']

    def __init__(self):
        self.r = RedisManager().rc

    def parse(self, response):
        url = response.url
        # if self.r.sismember(self.over_key, url):
        #     print("already crawl:{}".format(url))
        #     return
        self.r.sadd(self.over_key, url)
        t = response.xpath('//table[@class="dltable"]/tbody/tr[last()]/td/a/@href').extract()[0]
        info_dom = response.xpath('//div[@class="bookinfo"]/ul/li')
        name = info_dom[0].xpath('./a/text()').extract()
        if len(name) > 0:
            name = name[0]
        else:
            name = 'unknown'
        author = info_dom[1].xpath('./a/text()').extract()
        if len(author) > 0:
            author = author[0]
        else:
            author = 'unknown'
        d = info_dom[2].xpath('./a').xpath('string()').extract()
        date = info_dom[2].xpath('./text()').extract()
        if len(d) > 0:
            d = d[0]
        else:
            d = ''
        if len(date) > 0:
            date = '{}{}'.format(d, date[0])
            ts = time.strptime(date, "%Y-%m")
            date = time.strftime("%Y/%m/%d %H:%M:%S", ts)
        else:
            date = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        publisher = info_dom[3].xpath('./a/text()').extract()
        if len(publisher) > 0:
            publisher = publisher[0]
        else:
            publisher = 'unknown'
        isbn = info_dom[5].xpath('./text()').extract()
        if len(isbn) > 0:
            isbn = isbn[0]
        else:
            isbn = 'unknown'
        item = BookItem()
        item['name'] = name
        item['author'] = author
        item['publish_date'] = date
        item['publisher'] = publisher
        item['isbn'] = isbn
        item['url'] = t
        print(item)
        yield item
