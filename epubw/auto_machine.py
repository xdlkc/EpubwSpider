import os
import pickle
import time

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as ec, ui
from selenium.webdriver.support.wait import WebDriverWait

from tools import MysqlManager

BAIDU_NETDISK_COOKIE_PATH = 'baidu_netdisk.pickle'


def input_code(url, code, browser):
    """
    自动完成提取码填充和文件保存任务
    """
    cookies = read_cookies()
    try:
        print("start process url:{} and code:{}".format(url, code))
        browser.get(url)
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
        wait.until(ec.presence_of_all_elements_located(
            (By.CLASS_NAME, "slide-show-left")))
        print("open url success")
        # 选中所有文件
        browser.find_element_by_xpath('//*[@id="shareqr"]/div[2]/div[2]/div/ul[1]/li[1]/div/span[1]').click()
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
        print("save success url :{}".format(url))
    except Exception as e:
        print(e)
    finally:
        return


def get_cookies(url):
    """
    获取网盘cookie并写入cookie文件
    :param url:
    :return:
    """
    browser = webdriver.Chrome()
    browser.get(url)
    login_success_url = url + '?errno=0&errmsg=Auth%20Login%20Sucess&&bduss=&ssnerror=0&traceid=#list/path=%2F'
    while True:
        time.sleep(10)
        while browser.current_url == login_success_url:
            baidu_cookies = browser.get_cookies()
            browser.quit()
            cookies = {}
            for item in baidu_cookies:
                cookies[item['name']] = item['value']
            output_path = open(BAIDU_NETDISK_COOKIE_PATH, 'wb')
            pickle.dump(cookies, output_path)
            output_path.close()
            return cookies


def read_cookies():
    """
    读取cookie,若本地不存在，则手动登录一次即可
    """
    if os.path.exists(BAIDU_NETDISK_COOKIE_PATH):
        path = open(BAIDU_NETDISK_COOKIE_PATH, 'rb')
        cookies = pickle.load(path)
    else:
        # https://pan.baidu.com/s/1oE4gGe1Kn-jkuFhVR2aNJQ:id8a
        cookies = get_cookies('https://pan.baidu.com/s/1oE4gGe1Kn-jkuFhVR2aNJQ')
    return cookies


def read_books_url_and_code():
    """
    从DB读取网盘地址及提取码，读取规则自行更改
    """
    m = MysqlManager()
    return m.execute_query('select id,pan_url,secret from book limit 10;')


if __name__ == '__main__':
    r = read_books_url_and_code()
    browser = webdriver.Chrome()
    for ri in r:
        input_code(ri[1], ri[2], browser)
    browser.close()
