import time

from selenium.webdriver.common.by import By

from aiautomation.gui.page import Page
from aiautomation.testcase.decorator import component


class 登录页面(Page):

    用户名=(By.ID, "UserAccount")
    密码=(By.ID, "UserPwd")
    登录按钮=(By.ID, "loginIMG")

    @component("10")
    def 登录(self, username, password):
        browser = self.browser
        config = browser.config
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

        browser.find_element_by_locate(self.用户名).send_keys(username)
        browser.find_element_by_locate(self.密码).send_keys(password)

        time.sleep(0.5)
        browser.find_element_by_locate(self.登录按钮).click()
        time.sleep(1)