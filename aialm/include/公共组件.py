# coding: utf-8
import time

import sys
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.wait import WebDriverWait


class 公共组件:

    def __init__(self, page=None):
        self.page = page

    def 打开菜单(self, first_menu, second_menu, third_menu=None):
        browser = self.page.browser
        logger = self.page.logger
        logger.info("==================================")
        logger.info("=============打开菜单==============")
        # 登录完成之后，有可能document已经ready了，但是很多js代码是要注入的，导致不能执行
        time.sleep(1)

        browser.get_waiter(10).until(
            expected_conditions.presence_of_element_located((By.XPATH, "//em[text()='%s']/parent::li" % first_menu)))

        menu_level_one = browser.find_element_by_xpath("//em[text()='%s']/parent::li" % first_menu)
        menu_level_one.click()

        menu_level_two = browser.find_element_by_xpath("//a[text()='%s']" % second_menu)
        menu_level_two.click()

        if third_menu is not None:
            menu_level_three = browser.find_element_by_xpath("//ul[@class='third_menu']//a[text()='%s']" % third_menu)
            menu_level_three.click()
            menu_level_one.click()

        # 切换菜单，等待一下页面调入
        time.sleep(1)

    def Frame跳转到(self, *iframes):
        browser = self.page.browser
        browser.switch_to_default_content()
        for iframe in iframes:
            browser.switch_to.frame(browser.webdriver.find_element_by_xpath(iframe))
        self.page.default_iframe = iframes

    def Form输入框录入(self, name, value):
        self.page.browser.find_element_by_xpath("//td[text()='%s：']/following-sibling::td[1]//input" % name).input(
            value)

    def Form多行输入框录入(self, name, value):
        print(self.page.browser.find_element_by_xpath("//td[text()='%s：']/following-sibling::td[1]//textarea" % name))
        self.page.browser.find_element_by_xpath("//td[text()='%s：']/following-sibling::td[1]//textarea" % name).input(
            value)

    def From按钮点击(self, name):
        self.page.browser.find_element_by_xpath("//input[@value='%s']" % name).click()

    def From下拉框选择(self, name, option_text):
        self.page.browser.find_element_by_xpath(
            "//td[text()='%s：']/following-sibling::td[1]//select" % name).find_element_by_xpath(
            "//option[text()='%s']" % option_text).click()

    def AppFrame下拉框选择(self, name, option_text):
        self.page.browser.find_element_by_xpath("//td[text()='%s：']/following-sibling::td[1]/span" % name).fire_event(
            "onfocusin")
        self.page.browser.find_element_by_xpath(
            "//td[text()='%s：']/following-sibling::td[1]//select" % name).find_element_by_xpath(
            "//option[text()='%s']" % option_text).click()
        self.page.browser.find_element_by_xpath("//td[text()='%s：']/following-sibling::td[1]/span" % name).fire_event(
            "onfocusout")

    def AppFrame时间选择(self, name, input_date):
        """
        针对测试平台的日期插件My97DatePicker进行选择
        :param input_date:
        :param page:
        :param name:
        :return:
        """

        browser = self.page.browser
        date_array = input_date.split("-")
        year = date_array[0]
        month = date_array[1]
        day = date_array[2]
        browser.find_element_by_xpath("//td[text()='%s：']/following-sibling::td[1]//input" % name).click()
        browser.switch_to_frame(
            browser.webdriver.find_element_by_xpath("//iframe[contains(@src, 'My97DatePicker.htm')]"))
        browser.execute_script("day_Click(%s, %s, %s)" % (year, month, day))

    def 处理人弹出窗口确认(self, opion):

        browser = self.page.browser
        init_size = len(browser.window_handles)
        init_window = browser.current_window_handle
        browser.switch_to_window_by_title("选择人员")
        browser.find_element_by_xpath("//input[@value='确认']").fire_event('onclick')
        self.page.browser.logger.debug("等待窗口数量变为：%d" % (init_size - 1))
        browser.wait_windows_size_to_be(10, init_size - 1)
        browser.switch_to_window(init_window)

    def 测试平台人员选择(self, name, user_name):
        """
        选择人工具类
        :param browser:
        :param name:
        :param user_name:
        :return:
        """
        browser = self.page.browser

        init_size = len(browser.window_handles)
        init_window = browser.current_window_handle
        if name is not None:
            browser.find_element_by_xpath(
                "//td[starts-with(text(), '%s')]/parent::*//input[@type='button']" % name).click()
            WebDriverWait(browser.webdriver, 10).until(expected_conditions.number_of_windows_to_be(init_size + 1))
        else:
            time.sleep(0.5)

        browser.switch_to_windows_by_url("/SelectStaff")
        self.page.browser.logger.debug("人员选择窗口，并选择人员：%s" % user_name)
        browser.find_element_by_id("searchPerson").input(user_name)
        browser.find_element_by_id("qryBtn").fire_event("onclick")

        time.sleep(1)
        WebDriverWait(browser.webdriver, 5).until(
            expected_conditions.text_to_be_present_in_element((By.ID, "DataTable_staffTable"), user_name))

        browser.find_element_by_xpath("//*[@id='DataTable_staffTable']//td[text()='%s']/parent::*" % user_name).click()
        time.sleep(0.5)
        browser.find_element_by_xpath("//input[@value='确认']").click()
        if name is not None:
            self.page.browser.logger.debug("等待窗口数量变为：%d" % init_size)
            WebDriverWait(browser.webdriver, 10).until(expected_conditions.number_of_windows_to_be(init_size))
        else:
            self.page.browser.logger.debug("等待窗口数量变为：%d" % (init_size - 1))
            WebDriverWait(browser.webdriver, 10).until(expected_conditions.number_of_windows_to_be(init_size - 1))
        browser.switch_to_window(init_window)

    def 操作提示关闭(self):
        message = self.page.browser.find_element_by_xpath("//div[@class='panel window messager-window']").text
        self.page.browser.find_element_by_xpath(
            "//div[@class='panel window messager-window']//span[text()='确定']").click()
        self.page.slogger.debug("获得提示信息:%s" % message)
