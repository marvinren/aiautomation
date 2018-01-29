# coding: utf-8

from aiautomation.testcase.decorator import testcase
from aiautomation.testcase.test_case_module import TestCaseModule


class 需求录入(TestCaseModule):

    @testcase(case_id=3, module_id=8, case_exec_id=82)
    def 普通需求录入(self, data=None):
        from ..pages.登录 import 登录
        from ..pages.需求录入 import 需求录入
        
        self.create_page(登录).登录()
        self.create_page(需求录入).需求录入页面打开()
        self.create_page(需求录入).需求录入()
        self.create_page(需求录入).需求提交()
        self.create_page(需求录入).需求提交验证()

