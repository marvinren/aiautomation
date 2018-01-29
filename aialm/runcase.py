from aiautomation.log.simple_log import SimpleLog
from aiautomation.testcase.browser import Browser
from aiautomation.testcase.test_plan import PlanInfo, TestPlanRunner

t = TestPlanRunner()
# t.simple_run("需求查询", "需求查询测试案例")
# t.simple_run("需求录入", "普通需求录入")
# t.run_case_by_case_exec_id(62, 2)

t.simple_run("需求评审", "一般需求评审")