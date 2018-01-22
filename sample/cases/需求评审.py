from aiautomation.testcase.decorator import testcase
from aiautomation.testcase.test_case_module import TestCaseModule


class 需求评审(TestCaseModule):

    @testcase(case_id=3, module_id=22)
    def 需求评审通过(self):
        from ..pages.登录页面 import 登录页面
        from ..pages.主界面 import 主界面

        self.create_page(登录页面).登录("yekeke", "!ABcd1234")
        self.create_page(主界面).进入工单("测试工时统计")