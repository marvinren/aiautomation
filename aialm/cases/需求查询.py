# coding: utf-8

from aiautomation.testcase.decorator import testcase
from aiautomation.testcase.test_case_module import TestCaseModule


class 需求查询(TestCaseModule):

    @testcase(case_id=2, module_id=6, case_exec_id=100)
    def 需求查询测试案例(self, data=None):
        from ..pages.登录 import 登录
        from ..pages.需求查询 import 需求查询
        
        self.create_page(登录).登录()
        self.create_page(需求查询).打开需求查询菜单()
        self.create_page(需求查询).需求查询()

