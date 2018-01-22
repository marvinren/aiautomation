# coding: utf-8

from aiautomation.testcase.decorator import testcase
from aiautomation.testcase.test_case_module import TestCaseModule


class 需求查询(TestCaseModule):

    @testcase(case_id=1, module_id=22)
    def 按需求名称查询(self, data=None):
        from ..pages.登录页面 import 登录页面
        from ..pages.主界面 import 主界面
        from ..pages.需求查询页面 import 需求查询页面

        if data is None:
            data = {
                "需求名称": "测试工时统计"
            }
        self.create_page(登录页面).登录()
        self.create_page(主界面).打开菜单("综合查询", "需求查询")
        self.create_page(需求查询页面).需求查询(data)
        self.create_page(需求查询页面).查询结果校验(data)
