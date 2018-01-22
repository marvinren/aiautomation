from selenium.webdriver.common.by import By

from aiautomation.gui.page import PageObject
from aiautomation.testcase.decorator import component


class 百度搜索页面(PageObject):

    搜索输入框 = (By.ID, "kw")
    搜索按钮 = (By.ID, "su")

    @component(100)
    def 搜索关键字(self, data = None):
        search_text = "pages yeah"
        self.browser.find_element_by_locate(self.搜索输入框).send_keys(search_text)
        self.browser.find_element_by_locate(self.搜索按钮).click()
        self.browser.assert_check_point_true("校验是否包含查询的内容", self.browser.webdriver.title.find(search_text) >= 0)

