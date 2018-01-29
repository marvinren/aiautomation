# coding: utf-8
import time
from selenium.webdriver.common.by import By

from aiautomation.gui.page import Page
from aiautomation.testcase.decorator import component


class 需求审批(Page):
    待办工单 = (By.ID, "DataTable_waitWorkorder")

    @component(10001)
    def 选择需求工单(self, data=None):
        from ..include.公共组件 import 公共组件

        browser = self.browser
        common = 公共组件(self)
        common.Frame跳转到("//*[@id='mainFrame']", "//iframe", "//iframe")
        common.From下拉框选择("项目组", data["需求所属项目组"])
        time.sleep(0.5)
        browser.find_element_by_locate(self.待办工单).find_element_by_xpath("//td[text()='%s']" % data['需求名称']).dbl_click()

    @component(10000)
    def 需求审批提交(self, data=None):
        from ..include.公共组件 import 公共组件
        browser = self.browser

        common = 公共组件(self)
        common.Frame跳转到("//*[@id='mainFrame']", "//iframe[@id='contentFrame']",
                        "//iframe[contains(@src, 'com.asiainfo.aialmJT.testWF.web.AlmRequisitionAction')]")

        browser.find_element_by_xpath("//*[text()='需求计划']").click()
        browser.wait_windows_size_to_be(10, 2)
        common.处理人弹出窗口确认("")
        common.Frame跳转到("//*[@id='mainFrame']", "//iframe[@id='contentFrame']",
                        "//iframe[contains(@src, 'com.asiainfo.aialmJT.testWF.web.AlmRequisitionAction')]")
        common.操作提示关闭()
