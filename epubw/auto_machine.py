import os
import pickle
import time

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as ec, ui
from selenium.webdriver.support.wait import WebDriverWait

from tools import MysqlManager

BAIDU_NETDISK_COOKIE_PATH = 'epubw/resources/baidu_netdisk.pickle'


def auto_extract_file(url, code):
    browser = webdriver.Chrome()
    auto_extract_files(url, code, browser)
    browser.quit()


def auto_extract_files(url, code, browser):
    """
    自动完成提取码填充和文件保存任务
    """
    cookies = read_cookies(browser)
    try:
        print("start process url:{} and code:{}".format(url, code))
        browser.get(url)
        # 必须放在get之后，否则domain会提示非法
        for cookie in cookies:
            browser.add_cookie({
                "name": cookie,
                "value": cookies[cookie],
                "domain": ".pan.baidu.com",
                "path": "/"
            })
        print("set cookies success")
        input = browser.find_element_by_id('mwxxPOD')
        # 填入提取码并提交
        input.send_keys(code)
        input.send_keys(Keys.ENTER)

        # 等待文件列表页出现
        wait = WebDriverWait(browser, 10)
        wait.until(ec.presence_of_all_elements_located((By.CLASS_NAME, "slide-show-left")))
        print("open url success")
        # 选中所有文件
        browser.find_element_by_xpath('//li[@data-key="server_filename"]/div/span[1]').click()
        # 选中保存网盘按钮
        browser.find_element_by_xpath('//a[@title="保存到网盘"]/span/span').click()

        # 等待目录选中窗口出现
        wait = ui.WebDriverWait(browser, 10)
        wait.until(ec.presence_of_all_elements_located((By.ID, 'fileTreeDialog')))
        xf = browser.find_element_by_id('fileTreeDialog')
        # 最近保存目录
        # xf.find_element_by_class_name('save-path-item').click()
        time.sleep(1)
        # 选择目录
        path = "/test"
        xf.find_element_by_xpath('//span[@node-path="{}"]'.format(path)).click()
        # 确定保存
        xf.find_element_by_xpath('//a[@title="确定"]').click()
        time.sleep(3)
        print("save success url :{}\n".format(url))
    except Exception as e:
        print(e)
    finally:
        return


def read_cookies(browser):
    """
    读取cookie,若本地不存在，则手动登录一次即可
    """
    if os.path.exists(BAIDU_NETDISK_COOKIE_PATH):
        path = open(BAIDU_NETDISK_COOKIE_PATH, 'rb')
        cookies = pickle.load(path)
    else:
        cookies = get_cookies(browser, 'https://pan.baidu.com')
    return cookies


def get_cookies(browser, url):
    """
    获取网盘cookie并写入cookie文件
    :param url:
    :return:
    """
    browser.get(url)
    login_success_url = url + '/disk/home?errno=0&errmsg=Auth%20Login%20Sucess&&bduss=&ssnerror=0&traceid=#/all?path' \
                              '=%2F&vmode=list'
    while True:
        time.sleep(5)
        while browser.current_url == login_success_url:
            baidu_cookies = browser.get_cookies()
            cookies = {}
            for item in baidu_cookies:
                cookies[item['name']] = item['value']
            output_path = open(BAIDU_NETDISK_COOKIE_PATH, 'wb')
            pickle.dump(cookies, output_path)
            output_path.close()
            return cookies


def read_books_url_and_code(book_name):
    """
    从DB读取网盘地址及提取码，读取规则自行更改
    """
    m = MysqlManager()
    query_sql = 'select id,pan_url,secret,name,author,publish_date,publisher from book ' \
                'where pan_url is not null  and secret is not null and name like "%{}%" limit 2;'.format(book_name)
    print(query_sql)
    return m.execute_query(query_sql)


if __name__ == '__main__':
    r = read_books_url_and_code('参与感')
    # print(r)
    browser = webdriver.Chrome()
    for ri in r:
        auto_extract_files(ri[1], ri[2], browser)
    browser.quit()
