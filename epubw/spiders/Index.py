# -*- coding: utf-8 -*-
import scrapy
import re
from epubw.keys import *
from epubw.settings import *
from epubw.tools import RedisManager
from epubw.items import BookItem


# 首页爬虫：https://epubw.com/
class IndexSpider(scrapy.Spider):
    name = INDEX_SPIDER_NAME
    allowed_domains = ['epubw.com']
    # 网站初始页码，用于服务中断后的记录位置
    init_page = 20
    # 网站最大页数
    max_pages = 500
    default_url_prefix = 'https://epubw.com/page/'

    def __init__(self):
        self.r = RedisManager().rc
        self.start_urls = ["{}{}".format(self.default_url_prefix, self.init_page)]

    def parse(self, response):
        articles = response.xpath('//div[@class="row equal"]/article')
        # 逐条解析
        for article in articles:
            img = article.xpath('//img/@src')[0].extract()
            tmp = article.xpath('./div[@class="caption"]/p/a')
            name = tmp.xpath('./text()')[0].extract()
            link = tmp.xpath('./@href')[0].extract()
            # 推送redis队列
            self.r.lpush(BOOK_FIRST_URL_KEY, link)
            item = BookItem()
            item['name'] = name
            item['first_url'] = link
            item['img'] = img
            yield item
        url = response.url
        current_page = int(re.findall(self.default_url_prefix + '(\d+)', url)[0])
        print(current_page)
        if current_page < self.max_pages:
            current_page += 1
            yield scrapy.Request('{}{}'.format(self.default_url_prefix, current_page), callback=self.parse)
