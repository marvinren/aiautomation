import time
from selenium.webdriver.common.by import By

from aiautomation.gui.page import Page
from aiautomation.testcase.decorator import component


class 需求查询页面(Page):

    查询按钮 = (By.XPATH, "//input[@value='需求查询']")

    def switch_to_frame(self):
        browser = self.browser
        browser.switch_to_default_content()
        browser.switch_to_frame('mainFrame')
        browser.switch_to_frame(browser.find_element_by_tag_name("iframe"))

    @component(4)
    def 需求查询(self, data=None):
        from ..include.aialm_helper import input_tool
        self.switch_to_frame()
        input_tool(self.browser, "需求名称", data["需求名称"])
        self.browser.find_element_by_locate(self.查询按钮).click()
        self.logger.info("查询完毕")
        time.sleep(0.5)

    @component(5)
    def 查询结果校验(self, data=None):
        self.switch_to_frame()
        self.logger.info("点击完查询按钮，查询数据表的结果如下:")
        result = self.browser.find_element_by_id("DataTable_reqTable").text
        self.logger.info("表格结果为:\n%s" % result)
        self.browser.assert_check_point_true("查询存在查询条件的内容", result.find(data["需求名称"]) >= 0)
