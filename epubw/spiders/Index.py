# -*- coding: utf-8 -*-
import scrapy
import redis
from ..keys import *
from ..settings import PUBLIC_URL_PREFIX
from ..tools import RedisManager


# 分类浏览页面爬虫
class IndexSpider(scrapy.Spider):
    name = 'Index'
    allowed_domains = ['epubw.com/page']
    url_sets = set()
    init_page = 1

    def __init__(self):
        self.r = RedisManager().rc
        self.max_pages = 500
        self.start_urls = ["{}/page/{}".format(PUBLIC_URL_PREFIX, self.init_page)]
        # self.f = open('./resources/urls.txt', 'a+')

    def parse(self, response):
        meta = response.meta
        if meta is not None and 'page' in meta:
            page = meta['page']
        else:
            page = self.init_page
        print('crawl page:{}'.format(page))
        articles = response.xpath('//div[@class="row equal"]/article')
        for article in articles:
            link = article.xpath('./a/@href').extract()[0]
            # self.r.lpush(BOOK_FIRST_URL_KEY, link)
            self.r.sadd(BOOK_FIRST_URL_SET, link)
        page += 1
        meta['page'] = page
        if page < self.max_pages:
            yield scrapy.Request(url='https://epubw.com/page/{}'.format(page), meta=meta, callback=self.parse,
                                 dont_filter=True)

    # def closed(self, reason):
    #     for s in self.url_sets:
    #         self.f.write(s + "\n")
    #     print("crawl over, save file")
    #     self.f.close()
