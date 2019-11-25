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
    # 图书图片
    img = scrapy.Field()
    publish_date = scrapy.Field()
    publisher = scrapy.Field()
    isbn = scrapy.Field()
    # 一级地址
    first_url = scrapy.Field()
    # 二级地址
    second_url = scrapy.Field()
    # 三级地址
    third_url = scrapy.Field()
    # 网盘地址
    pan_url = scrapy.Field()
    # 网盘提取码
    secret = scrapy.Field()
