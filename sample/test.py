from aiautomation.testcase.test_plan import TestPlanRunner, PlanInfo

plan = PlanInfo('4', '自动化测试', None
                , None, '119', '1000', '0', '0')
t = TestPlanRunner(plan=plan)
t.add_case("需求查询", "按需求名称查询", "./datas/需求查询_按需求名称查询.csv")
t.add_case("需求录入", "普通需求录入")
t.add_case("需求评审", "")
t.start()


