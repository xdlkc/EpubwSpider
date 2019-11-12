import logging
from redis import Redis
from mysql.connector import pooling
from rediscluster import RedisCluster
import requests
from epubw.keys import *
import re

# mysql配置
MYSQL_CONFIG = {
    'pool_size': 10,
    'pool_reset_session': True,
    'host': '127.0.0.1',
    'port': '3306',
    'database': 'epubw',
    'user': 'root',
    'password': 'wimness.',
    'charset': 'utf8'
}
# redis集群配置
STARTUP_NODES = [{"host": "127.0.0.1", "port": "7000"}, {"host": "127.0.0.1", "port": "7001"},
                 {"host": "127.0.0.1", "port": "7002"}]


class MysqlManager(object):
    def __init__(self):
        self.mcp = pooling.MySQLConnectionPool(**MYSQL_CONFIG)

    def execute_dml(self, sql_str, *args):
        cnx = None
        try:
            cnx = self.mcp.get_connection()
            cursor = cnx.cursor()
            cursor.execute(sql_str, args)
            cursor.close()
            cnx.commit()
        except Exception as e:
            logging.log(logging.ERROR, e)
            raise e
        finally:
            if cnx:
                cnx.close()

    def execute_query(self, sql_str, *args):
        cnx = None
        try:
            cnx = self.mcp.get_connection()
            cursor = cnx.cursor()
            cursor.execute(sql_str, args)
            result_set = cursor.fetchall()
            cursor.close()
            return result_set
        except Exception as e:
            logging.log(logging.ERROR, "args:{},err:{}".format(args, e))
        finally:
            if cnx:
                cnx.close()


class RedisManager(object):
    def __init__(self):
        self.rc = Redis(decode_responses=True)


def fun():
    r = RedisManager().rc
    s = r.smembers(BOOK_FIRST_URL_SET)
    for si in s:
        print(si)
        r.lpush(BOOK_FIRST_URL_KEY, si)


def db_to_cache(queue_key):
    """
    将url写入待爬队列，同时将id映射放入hash
    :return:
    """
    db = MysqlManager()
    r = RedisManager().rc
    n = 0
    while True:
        sql = "select id,url from book where id > %s and url != '' and book.url is not null order by book.id limit 1000"
        rs = db.execute_query(sql, n)
        if len(rs) == 0:
            break
        for rsi in rs:
            id = rsi[0]
            url = rsi[1]
            if id > n:
                n = id
            # r.hset(BOOK_THIRD_ID_HASH, url, id)
            r.lpush(queue_key, url)
        print(n)


def request_url(url):
    s = requests.get(url).text
    print(s)


if __name__ == '__main__':
    # fun()
    db_to_cache(BOOK_THIRD_URL_KEY)
