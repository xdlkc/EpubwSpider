# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
from .tools import MysqlManager
from epubw.keys import *


class BookPipeline(object):
    def __init__(self):
        self.m = MysqlManager()

    def process_item(self, item, spider):
        print(item)
        if spider.name == INDEX_SPIDER_NAME:
            sql = "insert into book (name, first_url,img) values (%s, %s, %s);"
            self.m.execute_dml(sql, item[NAME], item[FIRST_URL], item[IMG])
        elif spider.name == FIRST_BOOK_SPIDER_NAME:
            sql = "update book set author=%s,publish_date=%s,publisher=%s,second_url=%s,isbn=%s where first_url=%s;"
            self.m.execute_dml(sql, item[AUTHOR], item[PUBLISH_DATE], item[PUBLISHER], item[SECOND_URL],
                               item[ISBN], item[FIRST_URL])
        elif spider.name == SECOND_BOOK_SPIDER_NAME:
            sql = "update book set third_url=%s,secret=%s where second_url=%s;"
            self.m.execute_dml(sql, item[THIRD_URL], item[SECRET], item[SECOND_URL])
        elif spider.name == THIRD_BOOK_SPIDER_NAME:
            sql = "update book set pan_url=%s where third_url=%s;"
            self.m.execute_dml(sql, item[PAN_URL], item[THIRD_URL])
        else:
            print("wow! we find a new unknown spider")
