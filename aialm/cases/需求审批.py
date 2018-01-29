# coding: utf-8

from aiautomation.testcase.decorator import testcase
from aiautomation.testcase.test_case_module import TestCaseModule


class 需求评审(TestCaseModule):
    @testcase(case_id=3, module_id=6, case_exec_id=10000)
    def 一般需求评审(self, data=None):
        from ..pages.登录 import 登录
        from ..pages.需求审批 import 需求审批

        data = {
            "登录用户名": "yekeke",
            "登录密码": "!ABcd1234",
            "需求所属项目组": "一级开发测试平台",
            "需求名称": "TESTREQ20180122003617"
        }

        self.create_page(登录).登录(data)
        self.create_page(需求审批).选择需求工单(data)
        self.create_page(需求审批).需求评审提交(data)
