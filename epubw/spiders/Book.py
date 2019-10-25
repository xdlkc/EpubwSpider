# -*- coding: utf-8 -*-
import scrapy
from scrapy_redis.spiders import RedisSpider


class BookSpider(RedisSpider):
    name = 'Book'
    redis_key = 'epubw:book_url'
    allowed_domains = ['epubw.com']

    def parse(self, response):
        t = response.xpath('//table[@class="dltable"]/tbody/tr[last()]/td/a/@href').extract()[0]
        print(t)
