from aiautomation.testcase.test_plan import TestPlanRunner, PlanInfo

plan = PlanInfo('4', '自动化测试', None
                , None, '119', '1000', '0', '0')

t = TestPlanRunner(plan=plan)
t.add_case("百度搜索", "一般百度搜索")
t.start()
