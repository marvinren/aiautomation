# coding: utf-8
import time
from selenium.webdriver.common.by import By

from aiautomation.gui.page import Page
from aiautomation.testcase.decorator import component


class 需求查询(Page):

    @component(3)
    def 需求查询(self, data=None):
        from ..include.公共组件 import 公共组件
        
        common = 公共组件(self)
        common.Frame跳转到("//*[@id='mainFrame']", "//iframe")
        common.Form输入框录入("需求名称", "测试工时")
        common.From按钮点击("需求查询")

    @component(5)
    def 打开需求查询菜单(self, data=None):
        from ..include.公共组件 import 公共组件
        
        common = 公共组件(self)
        common.打开菜单("综合查询", "需求查询")

    @component(6)
    def 需求查询结果校验(self, data=None):
        from ..include.公共组件 import 公共组件
        公共组件(self).Frame跳转到("//*[@id='mainFrame']", "//iframe")
        
        self.logger.info("点击完查询按钮，查询数据表的结果如下:")
        result = self.browser.find_element_by_id("DataTable_reqTable").text
        self.logger.info("表格结果为:\n%s" % result)
        self.browser.assert_check_point_true("查询存在查询条件的内容", result.find(data["需求名称"]) >= 0)


