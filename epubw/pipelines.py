# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
from .tools import MysqlManager


class EpubwPipeline(object):
    def process_item(self, item, spider):
        return item


class BookPipeline(object):
    def __init__(self):
        self.m = MysqlManager()

    def process_item(self, item, spider):
        print(item)
        sql = "insert into epubw.book (name, author, publish_date, first_url, isbn, publisher) values (%s, %s, %s, %s, %s, %s)"
        self.m.execute_dml(sql, item['name'], item['author'], item['publish_date'], item['url'], item['isbn'],
                           item['publisher'])
