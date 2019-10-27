# -*- coding: utf-8 -*-
import scrapy
import redis


class IndexSpider(scrapy.Spider):
    name = 'Index'
    allowed_domains = ['epubw.com/page']
    start_urls = ['https://epubw.com/page/34']
    url_sets = set()
    init_page = 300

    def __init__(self):
        self.r = redis.Redis(host='localhost', port=6379, decode_responses=True)
        self.max_pages = 500
        self.f = open('./resources/urls.txt', 'a+')

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
            info = article.xpath('./div[@class="caption"]/p')
            name = info[0].xpath('./a[1]/text()').extract()
            if len(name) > 0:
                name = name[0]
            else:
                name = ''
            author = info[1].xpath('./a[1]/text()').extract()
            if len(author) > 0:
                author = author[0]
            else:
                author = ''
            self.url_sets.add("{} {} {}".format(link, name, author))
        page += 1
        meta['page'] = page
        if page < self.max_pages:
            yield scrapy.Request(url='https://epubw.com/page/{}'.format(page), meta=meta, callback=self.parse,
                                 dont_filter=True)

    def closed(self, reason):
        for s in self.url_sets:
            self.f.write(s + "\n")
        print("crawl over, save file")
        self.f.close()


if __name__ == '__main__':
    s = 'https://epubw.com/320045.html'

