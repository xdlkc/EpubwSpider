import redis


def fun(fp):
    """
    将一级书籍地址存入scrapy_redis的待爬取队列
    :param fp:
    :return:
    """
    r = redis.Redis(host='localhost', port=6379, decode_responses=True)
    with open(fp, 'r') as f:
        for fi in f.readlines():
            r.lpush('epubw:book_url', fi.split(" ")[0])


def fun2():
    r = redis.Redis(host='localhost', port=6379, decode_responses=True)
    s = r.smembers('epubw:second_book_url')
    for si in s:
        print(si)
        r.lpush('epubw:second_book_url_list', si)


if __name__ == '__main__':
    # fun('/Users/ZhangJunbo/Code/epubw/epubw/resources/urls.txt')
    fun2()