# coding: utf-8
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.wait import WebDriverWait

from aiautomation.testcase.decorator import component, testcase
from aiautomation.testcase.test_case import TestCase
from ..include.common_component import CommonCase


class 需求查询(TestCase):

    @component(2)
    def 需求查询(self, data = None):
        browser = self.browser
        WebDriverWait(browser, 10).until(
            expected_conditions.presence_of_element_located((By.XPATH, "//iframe[@id='mainFrame']"))
        )

        from ..include.aialm_helper import select_tool, iframe_to_main
        # 自动切换到主iframe中去，PS：需要注意其他案例中的iframe跳转
        iframe_to_main(browser)
        # 还有一层嵌套的iframe
        browser.switch_to_frame(browser.find_element_by_tag_name("iframe"))

        browser.find_element_by_xpath("//td[text()='需求名称：']/following-sibling::td[1]//input").input(data["需求名称"])
        browser.execute_script(browser.find_element_by_xpath("//input[@value='需求查询']").get_attribute("onclick"))
        self.logger.info("点击完查询按钮，查询数据表的结果如下:")
        result = browser.find_element_by_id("DataTable_reqTable").text
        self.logger.info("表格结果为:\n%s" % result)

    @testcase(case_id=1, case_exec_id=1, node_id=0, case_name=None, module_name=None)
    def 测试案例1(self, data=None):
        common = CommonCase(self)
        common.打开菜单("综合查询", "需求查询")
        self.需求查询(data)

    @testcase(case_id=2, case_exec_id=2, node_id=0, case_name=None, module_name=None)
    def 测试案例2(self, data=None):
        common = CommonCase(self)
        common.打开菜单("综合查询", "需求查询")
        self.需求查询(data)
