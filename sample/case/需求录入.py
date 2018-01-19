# coding: utf-8
import time

from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.wait import WebDriverWait

from aiautomation.testcase.decorator import component, testcase
from aiautomation.testcase.test_case import TestCase
from ..include.common_component import CommonCase


class 需求录入(TestCase):

    @component(3)
    def 录入需求(self, data=None):
        browser = self.browser

        from ..include.aialm_helper import select_tool, iframe_to_main, calc_select, select_user
        # 自动切换到主iframe中去，PS：需要注意其他案例中的iframe跳转
        iframe_to_main(browser)

        #录入基本信息
        browser.find_element_by_xpath("//td[text()='需求名称：']/following-sibling::td[1]//input").input("自动化测试需求")
        browser.find_element_by_xpath("//td[text()='主题词：']/following-sibling::td[1]//input").input("测试")
        browser.find_element_by_xpath("//td[text()='需求描述：']/following-sibling::td[1]//textarea").input("自动化测试")
        select_tool(browser, "优先级", "中")
        select_tool(browser, "重要性", "中")
        select_tool(browser, "需求来源", "省公司")
        select_tool(browser, "需求类型", "系统优化")
        browser.find_element_by_xpath("//td[text()='项目组：']/following-sibling::td[1]//select").find_element_by_xpath(
            "//option[text()='一级开发测试平台']").click()
        browser.find_element_by_xpath("//td[text()='预估工作量：']/following-sibling::td[1]//input").input("30")

        calc_select(browser, "计划完成时间", 2018, 3, 5)
        iframe_to_main(browser)

        calc_select(browser, "需求提出时间", 2018, 1, 5)
        iframe_to_main(browser)

        # 选择相关人员
        iframe_to_main(browser)
        select_user(browser, "需求计划", "任志强")
        iframe_to_main(browser)
        select_user(browser, "功能测试", "吴丹")
        iframe_to_main(browser)
        select_user(browser, "联调测试", "吴丹")
        iframe_to_main(browser)
        select_user(browser, "版本发布", "陈振")
        iframe_to_main(browser)

        # 提交需求审核
        browser.find_element_by_xpath("//*[contains(text(), '需求审核')]/parent::*").click()
        select_user(browser, None, "叶可可")
        iframe_to_main(browser)

        WebDriverWait(browser, 7).until(expected_conditions.visibility_of_element_located((By.XPATH, "//div[@class='panel window messager-window']")))
        print(browser.find_element_by_xpath("//div[@class='panel window messager-window']").text)
        browser.find_element_by_xpath("//div[@class='panel window messager-window']//span[text()='确定']").click()

        import pdb
        pdb.set_trace()

    @testcase(case_id=3, case_exec_id=3, node_id=0, case_name=None, module_name=None)
    def 普通需求录入(self, data=None):
        common = CommonCase(self)
        common.打开菜单("我的工作区", "需求管理", "需求录入")
        self.录入需求(data)
