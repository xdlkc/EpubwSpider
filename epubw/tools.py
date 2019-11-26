import logging

from mysql.connector import pooling
from redis import Redis

from epubw.settings import REDIS_HOST, REDIS_PORT

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
        self.rc = Redis(host=REDIS_HOST, port=REDIS_PORT,
                        decode_responses=True)
