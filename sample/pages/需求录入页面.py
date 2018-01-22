import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.wait import WebDriverWait

from aiautomation.gui.page import Page
from aiautomation.testcase.decorator import component


class 需求录入页面(Page):

    项目组 = (By.XPATH, "//td[text()='项目组：']/following-sibling::td[1]//select")
    预估工作量 = (By.XPATH, "//td[text()='预估工作量：']/following-sibling::td[1]//input")
    提交提示框 = (By.XPATH, "//div[@class='panel window messager-window']")
    提交提示框_确认 = (By.XPATH, "//div[@class='panel window messager-window']//span[text()='确定']")

    def switch_to_frame(self):
        browser = self.browser
        browser.switch_to_default_content()
        browser.switch_to_frame('mainFrame')

    @component(3)
    def 录入需求(self, data=None):
        from ..include.aialm_helper import select_tool, calc_select, select_user, input_tool, input_textarea_tool
        self.switch_to_frame()

        input_tool(self.browser, "需求名称", data['需求名称'])
        input_tool(self.browser, "主题词", data['主题词'])
        input_textarea_tool(self.browser, "需求描述", data['需求描述'])
        select_tool(self.browser, "优先级", data['优先级'])
        select_tool(self.browser, "重要性", data['重要性'])
        select_tool(self.browser, "需求来源", data['需求来源'])
        select_tool(self.browser, "需求类型", data['需求类型'])
        self.browser.find_element_by_locate(self.项目组).select(data["项目组"])
        self.browser.find_element_by_locate(self.预估工作量).input(data["预估工作量"])
        calc_select(self, "需求提出时间", data['需求提出时间'])
        calc_select(self, "计划完成时间", data['计划完成时间'])

        select_user(self, "需求计划", data['需求计划人员'])
        select_user(self, "功能测试", data['功能测试人员'])
        select_user(self, "联调测试", data["联调测试人员"])
        self.browser.find_element_by_xpath("//*[contains(text(), '需求审核')]/parent::*").click()
        select_user(self, None, data["需求审核人员"])

        self.browser.get_waiter(7).until(expected_conditions.visibility_of_element_located(self.提交提示框))
        message = self.browser.find_element_by_locate(self.提交提示框).text
        self.browser.assert_check_point_true("判断是否成功提交", message.find("提交成功") >= 0)
        self.browser.find_element_by_locate(self.提交提示框_确认).click()

