# coding: utf-8

from aiautomation.testcase.decorator import testcase
from aiautomation.testcase.test_case_module import TestCaseModule


class 空测试用例(TestCaseModule):

    @testcase(case_id=4, module_id=10, case_exec_id=149)
    def 空测试用例(self, data=None):
        from ..pages.空组件 import 空组件
        
        self.create_page(空组件).空组件(data)

