# -*- coding: utf-8 -*-
import scrapy

from epubw.keys import *
from epubw.settings import *
from epubw.tools import RedisManager
from epubw.items import BookItem


# 首页爬虫：https://epubw.com/
class IndexSpider(scrapy.Spider):
    name = INDEX_SPIDER_NAME
    allowed_domains = ['epubw.com']
    # 网站初始页码，用于服务中断后的记录位置
    init_page = 1
    # 网站最大页数
    max_pages = 500

    def __init__(self):
        self.r = RedisManager().rc
        self.start_urls = ["{}/page/{}".format(PUBLIC_URL_PREFIX, self.init_page)]

    def parse(self, response):
        meta = response.meta
        # 首次触发
        if meta is not None and 'page' in meta:
            page = meta['page']
        else:
            page = self.init_page
        print('crawl page:{}'.format(page))
        articles = response.xpath('//div[@class="row equal"]/article')
        # 逐条解析
        for article in articles:
            link = article.xpath('./a/@href').extract()[0]
            name = article.xpath('./div[@class="caption"]/p/a/text()').extract()[0]
            img = article.xpath('./a/img/@src').extract()[0]
            # 推送redis队列
            self.r.lpush(BOOK_FIRST_URL_KEY, link)
            item = BookItem()
            item['name'] = name
            item['first_url'] = link
            item['img'] = img
            yield item
        page += 1
        meta['page'] = page
        if page < self.max_pages:
            # 爬取下一页
            yield scrapy.Request(url='https://epubw.com/page/{}'.format(page), meta=meta, callback=self.parse,
                                 dont_filter=True)
