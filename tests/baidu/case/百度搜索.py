from aiautomation.testcase.decorator import component, testcase
from aiautomation.testcase.test_case_module import TestCaseModule


class 百度搜索(TestCaseModule):

    @testcase(case_id=8, module_id=22)
    def 一般百度搜索(self, data=None):
        from tests.baidu.gui.百度搜索页面 import 百度搜索页面
        page = 百度搜索页面(browser=self.browser)
        page.搜索关键字(data)
