# coding: utf-8
import time
from selenium.webdriver.common.by import By

from aiautomation.gui.page import Page
from aiautomation.testcase.decorator import component


class 登录(Page):

    @component(4)
    def 登录(self, data=None):
        import time
        browser = self.browser
        config = browser.config
        
        if data is not None:
            username = data['登录用户名']
            password = data['登录密码']
        
        try:
            if username is None or password is None:
                username = config.aiautomation.application.username
                password = config.aiautomation.application.password
        except:
            username = "administrator"
            password = "AAbbcc123"
        
        try:
            url = config.aiautomation.application.url
        except:
            url = "http://10.12.1.30:28080/aialm"
        
        browser.get(url)
        browser.maximize_window()
        time.sleep(0.5)
        
        browser.find_element_by_id("UserAccount").send_keys(username)
        browser.find_element_by_id("UserPwd").send_keys(password)
        
        time.sleep(0.5)
        browser.find_element_by_id("loginIMG").click()
        time.sleep(1)


