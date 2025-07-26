import os
import shelve

import pytest
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from time import sleep


@pytest.fixture(scope='session')
def get_driver():
    """创建浏览器实例的公共方法"""
    driver_path = r"/136.0.7103.49/chromedriver.exe"
    driver = webdriver.Chrome(service=Service(executable_path=driver_path))
    driver.maximize_window()
    try:
        driver.get("https://work.weixin.qq.com/wework_admin/frame#index")
        sleep(15)  # 留出充足时间扫码登录

        # 获取并处理 Cookie
        cookies = driver.get_cookies()
        cleaned_cookies = []
        for cookie in cookies:
            # 移除会导致问题的 expiry 字段（如果有）
            if 'expiry' in cookie:
                del cookie['expiry']
            cleaned_cookies.append(cookie)

        # 持久化存储到 shelve
        with shelve.open('../mydbs/cookies') as db: #确保mydbs目录存在
            db['cookies'] = cleaned_cookies  # 使用明确的键名
            print("Cookies 保存成功")
        yield driver

    finally:
        driver.quit()



class TestCookiePersistence:

    def test_reuse_cookies(self,get_driver):
        # path = os.path.dirname(os.path.dirname(__file__))
        # full_path = os.path.join(path, "mydbs/cookies")
        """复用存储的 Cookie"""
        # 从 shelve 加载 Cookie
        with shelve.open("../mydbs/cookies") as db:
            if 'cookies' not in db:
                raise ValueError("未找到存储的 Cookies，请先运行 test_save_cookies")
            cookies = db['cookies']

        # 添加 Cookie 到浏览器
        for cookie in cookies:
            get_driver.add_cookie(cookie)
        #打开带有cookie信息的页面
        get_driver.get("https://work.weixin.qq.com/wework_admin/frame#contacts")
        sleep(5)


