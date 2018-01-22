from aiautomation.testcase.decorator import testcase
from aiautomation.testcase.test_case_module import TestCaseModule


class 需求录入(TestCaseModule):

    @testcase(case_id=3, module_id=22)
    def 普通需求录入(self, data=None):
        from ..pages.主界面 import 主界面
        from ..pages.需求录入页面 import 需求录入页面
        from ..pages.登录页面 import 登录页面

        if data is None:
            data = {
                "需求名称": "测试工时统计",
                "主题词": "测试",
                "需求描述": "需求描述",
                "优先级": "中",
                "重要性": "中",
                "需求来源": "省公司",
                "需求类型": "系统优化",
                "项目组": '一级开发测试平台',
                "预估工作量": 30,
                "计划完成时间": "2018-6-1",
                "需求提出时间": "2018-1-1",
                "需求计划人员": "任志强",
                "功能测试人员": "吴丹",
                "联调测试人员": "吴丹",
                "需求审核人员": "叶可可"
            }
            
        self.create_page(登录页面).登录()
        self.create_page(主界面).打开菜单("我的工作区", "需求管理", "需求录入")
        self.create_page(需求录入页面).录入需求(data)