# -*- coding: utf-8 -*-
import redis
import scrapy
from scrapy_redis.spiders import RedisSpider


class BookSpider(RedisSpider):
    name = 'Book'
    redis_key = 'epubw:book_url'
    over_key = 'epubw:over_book'
    second_book_key = 'epubw:second_book_url'
    allowed_domains = ['epubw.com']

    def __init__(self):
        self.r = redis.Redis(host='localhost', port=6379, decode_responses=True)

    def parse(self, response):
        url = response.url
        if self.r.sismember(self.over_key, url):
            return
        self.r.sadd(self.over_key, url)
        t = response.xpath('//table[@class="dltable"]/tbody/tr[last()]/td/a/@href').extract()[0]
        print(t)
        self.r.sadd(self.second_book_key, t)
