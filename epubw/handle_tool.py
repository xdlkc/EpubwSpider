from keys import BOOK_FIRST_URL_KEY
from tools import MysqlManager, RedisManager


class HandleTool(object):
    def __init__(self):
        self.m = MysqlManager()
        self.r = RedisManager().rc

    def push_first(self):
        """
        推送一级url未爬取的书籍
        :return:
        """
        query_sql = 'select first_url from book where second_url is null;'
        r = self.m.execute_query(query_sql)
        for ri in r:
            # 推送redis队列
            self.r.lpush(BOOK_FIRST_URL_KEY, ri[0])


if __name__ == '__main__':
    ht = HandleTool()
    ht.push_first()
