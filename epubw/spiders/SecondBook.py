# -*- coding: utf-8 -*-
import redis
import scrapy
from scrapy_redis.spiders import RedisSpider
import re


class SecondbookSpider(RedisSpider):
    name = 'SecondBook'
    redis_key = 'epubw:second_book_url_list'
    over_key = 'epubw:over_second_book'
    last_book_set = set()
    allowed_domains = ['epubw.com']

    def __init__(self):
        self.r = redis.Redis(host='localhost', port=6379, decode_responses=True)
        self.f = open('./resources/books.txt', 'a+')

    def parse(self, response):
        url = response.url
        if self.r.sismember(self.over_key, url):
            return
        self.r.sadd(self.over_key, url)
        link = response.xpath('//div[@class="list"]/a/@href').extract()[0]
        name = response.xpath('//div[@class="desc"]/p/text()').extract()[0]
        name = re.findall('文件名称：《(.*)》', name)[0]
        print('{} {}'.format(link, name))
        self.last_book_set.add('{} {}'.format(name, link))

    def closed(self, reason):
        for s in self.url_sets:
            self.f.write(s + "\n")
        print("crawl over, save file")
        self.f.close()
