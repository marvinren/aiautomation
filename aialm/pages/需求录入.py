# coding: utf-8
import time
from selenium.webdriver.common.by import By

from aiautomation.gui.page import Page
from aiautomation.testcase.decorator import component


class 需求录入(Page):

    @component(7)
    def 需求录入(self, data=None):
        from selenium.webdriver.support import expected_conditions
        from ..include.公共组件 import 公共组件
        common = 公共组件(self)
        common.Frame跳转到("//iframe[@id='mainFrame']")
        common.Form输入框录入("需求名称", "测试需求1")
        common.Form输入框录入("主题词", "测试")
        common.Form多行输入框录入("需求描述", "测试需求")
        common.AppFrame下拉框选择("优先级", "中")
        common.AppFrame下拉框选择("重要性", "中")
        common.AppFrame下拉框选择("需求来源", "省公司")
        common.AppFrame下拉框选择("需求类型", "系统优化")
        
        common.From下拉框选择("项目组", "一级开发测试平台")
        common.Form输入框录入("预估工作量", "30")
        
        common.AppFrame时间选择("计划完成时间", "2018-07-01")
        common.Frame跳转到("//*[@id='mainFrame']")
        common.AppFrame时间选择("需求提出时间", "2018-01-01")
        common.Frame跳转到("//*[@id='mainFrame']")
        
        common.测试平台人员选择("需求计划", "任志强")
        common.Frame跳转到("//*[@id='mainFrame']")
        common.测试平台人员选择("功能测试", "吴丹")
        common.Frame跳转到("//*[@id='mainFrame']")
        common.测试平台人员选择("联调测试", "吴丹")
        common.Frame跳转到("//*[@id='mainFrame']")

    @component(8)
    def 需求录入页面打开(self, data=None):
        from ..include.公共组件 import 公共组件
        
        common = 公共组件(self)
        common.打开菜单("我的工作区", "需求管理", "需求录入")

    @component(9)
    def 需求提交(self, data=None):
        from selenium.webdriver.support import expected_conditions
        from ..include.公共组件 import 公共组件
        
        common = 公共组件(self)
        self.browser.find_element_by_xpath("//*[contains(text(), '需求审核')]/parent::*").click()
        self.browser.get_waiter(10).until(expected_conditions.number_of_windows_to_be(2))
        common.测试平台人员选择(None, "叶可可")
        common.Frame跳转到("//*[@id='mainFrame']")
        self.browser.get_waiter(7).until(expected_conditions.visibility_of_element_located((By.XPATH,  "//div[@class='panel window messager-window']")))
        message = self.browser.find_element_by_xpath("//div[@class='panel window messager-window']").text
        self.logger.debug("获得提示信息:%s" % message)
        self.browser.assert_check_point_true("判断是否成功提交", message.find("提交成功") >= 0)
        self.browser.find_element_by_xpath("//div[@class='panel window messager-window']//span[text()='确定']").click()

    @component(10)
    def 需求提交验证(self, data=None):
        pass


