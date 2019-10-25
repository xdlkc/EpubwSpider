# -*- coding: utf-8 -*-
import scrapy
import redis


class IndexSpider(scrapy.Spider):
    name = 'Index'
    allowed_domains = ['epubw.com/page']
    start_urls = ['https://epubw.com/page/2']
    url_sets = set()

    def __init__(self):
        self.r = redis.Redis(host='localhost', port=6379, decode_responses=True)

        self.f = open('/Users/ZhangJunbo/Code/epubw/epubw/resources/first_urls.txt', 'a+')

    def parse(self, response):
        meta = response.meta
        page = 1
        if meta is not None and 'page' in meta:
            page = meta['page']
        print('crawl page:{}'.format(page))
        articles = response.xpath('//div[@class="row equal"]/article')
        for article in articles:
            link = article.xpath('./a/@href').extract()[0]
            info = article.xpath('./div[@class="caption"]/p')
            name = info[0].xpath('./a[1]/text()').extract()[0]
            author = info[1].xpath('./a[1]/text()').extract()
            if len(author) > 0:
                author = author[0]
            else:
                author = ''
            print(link, name, author)
        #     for l in links:
        #         self.url_sets.add(l)
        #         self.r.lpush(l)
        # page += 1
        # meta['page'] = page
        # if page < 30:
        #     yield scrapy.Request(url='https://epubw.com/page/{}'.format(page), meta=meta, callback=self.parse,
        #                          dont_filter=True)

    def closed(self, reason):
        for s in self.url_sets:
            self.f.write(s + "\n")
        print("crawl over, save file")
        self.f.close()


if __name__ == '__main__':
    s = 'https://epubw.com/320045.html'
    r = redis.Redis(host='localhost', port=6379, decode_responses=True)
    r.lpush('epubw:book_url', s)
