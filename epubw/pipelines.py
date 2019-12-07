# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
from .tools import MysqlManager,RedisManager
from epubw.keys import *


class BookPipeline(object):
    def __init__(self):
        self.m = MysqlManager()
        self.r = RedisManager().rc

    def process_item(self, item, spider):
        print(item)
        if spider.name == INDEX_SPIDER_NAME:
            query_sql = 'select * from book where first_url=%s;'
            r = self.m.execute_query(query_sql, item[FIRST_URL])
            if len(r) > 0:
                return
            print("insert new book, name:{}".format(item[NAME]))
            # 推送redis队列
            self.r.lpush(BOOK_FIRST_URL_KEY, item[FIRST_URL])
            sql = "insert into book (name, first_url,img) values (%s, %s, %s);"
            self.m.execute_dml(sql, item[NAME], item[FIRST_URL], item[IMG])

        elif spider.name == FIRST_BOOK_SPIDER_NAME:
            # 推送二级地址到redis队列
            self.r.lpush(BOOK_SECOND_URL_KEY, item[SECOND_URL])
            sql = "update book set author=%s,publish_date=%s,publisher=%s,second_url=%s,isbn=%s where first_url=%s;"
            self.m.execute_dml(sql, item[AUTHOR], item[PUBLISH_DATE], item[PUBLISHER], item[SECOND_URL],
                               item[ISBN], item[FIRST_URL])

        elif spider.name == SECOND_BOOK_SPIDER_NAME:
            # 推送三级地址至redis队列
            self.r.lpush(BOOK_THIRD_URL_KEY, item[THIRD_URL])
            sql = "update book set third_url=%s,secret=%s where second_url=%s;"
            self.m.execute_dml(sql, item[THIRD_URL], item[SECRET], item[SECOND_URL])

        elif spider.name == THIRD_BOOK_SPIDER_NAME:
            sql = "update book set pan_url=%s where third_url=%s;"
            self.m.execute_dml(sql, item[PAN_URL], item[THIRD_URL])

        else:
            print("wow! we find a new unknown spider")
