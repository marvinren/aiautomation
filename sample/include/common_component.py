import time

from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC, expected_conditions

from aiautomation.testcase.decorator import component
from aiautomation.testcase.test_case import TestCase


class CommonCase(TestCase):

    def __init__(self, running_case):
        TestCase.__init__(self, scenarios_recovery=running_case._scenarios_recovery,
                          logger=running_case.logger, config=running_case.config, browser=running_case.browser)

    @component(0)
    def 打开菜单(self, first_menu, second_menu, third_menu=None):
        browser = self.browser
        logger = self.logger

        logger.info("=============打开菜单==============")
        # 登录完成之后，有可能document已经ready了，但是很多js代码是要注入的，导致不能执行
        time.sleep(1)
        WebDriverWait(browser, 10).until(
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
