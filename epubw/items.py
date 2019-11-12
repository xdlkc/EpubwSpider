# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class EpubwItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass


class BookItem(scrapy.Item):
    name = scrapy.Field()
    author = scrapy.Field()
    publish_date = scrapy.Field()
    publisher = scrapy.Field()
    url = scrapy.Field()
    isbn = scrapy.Field()
