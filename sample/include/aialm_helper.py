import time

from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.wait import WebDriverWait


def select_tool(browser, name, option_text):
    """
    针对测试平台的下拉框定制的工具方法
    :param browser:
    :param name:
    :param option_text:
    :return:
    """
    browser.find_element_by_xpath("//td[text()='%s：']/following-sibling::td[1]/span" % name).fire_event(
        "onfocusin")
    browser.find_element_by_xpath(
        "//td[text()='%s：']/following-sibling::td[1]//select" % name).find_element_by_xpath(
        "//option[text()='%s']" % option_text).click()
    browser.find_element_by_xpath("//td[text()='%s：']/following-sibling::td[1]/span" % name).fire_event(
        "onfocusout")


def iframe_to_main(browser):
    """
    针对测试平台将iframe指向main Iframe
    :param browser:
    :return:
    """
    browser.switch_to_default_content()
    browser.switch_to_frame(browser.find_element_by_xpath("//iframe[@id='mainFrame']"))


def calc_select(browser, name, year, month, day):
    """
    针对测试平台的日期插件My97DatePicker进行选择
    :param browser:
    :param name:
    :param year:
    :param month:
    :param day:
    :return:
    """
    browser.find_element_by_xpath("//td[text()='%s：']/following-sibling::td[1]//input" % name).click()
    browser.switch_to_frame(browser.find_element_by_xpath("//iframe[contains(@src, 'My97DatePicker.htm')]"))
    browser.execute_script("day_Click(%s, %s, %s)" % (year, month, day))


def select_user(browser, name, user_name):
    """
    选择人工具类
    :param browser:
    :param name:
    :param user_name:
    :return:
    """
    if name is not None:
        browser.find_element_by_xpath("//td[starts-with(text(), '%s')]/parent::*//input[@type='button']" % name).click()

    WebDriverWait(browser, 10).until(expected_conditions.number_of_windows_to_be(2))
    if browser.window_handles[0] == browser.current_window_handle:
        browser.switch_to_window(browser.window_handles[1])
    else:
        browser.switch_to_window(browser.window_handles[0])

    browser.find_element_by_id("searchPerson").input(user_name)
    browser.find_element_by_id("qryBtn").fire_event("onclick")

    time.sleep(1)
    WebDriverWait(browser, 5).until(
        expected_conditions.text_to_be_present_in_element((By.ID, "DataTable_staffTable"), user_name))

    browser.find_element_by_xpath("//*[@id='DataTable_staffTable']//td[text()='%s']/parent::*" % user_name).click()
    time.sleep(0.5)
    browser.find_element_by_xpath("//input[@value='确认']").click()
    WebDriverWait(browser, 3).until(expected_conditions.number_of_windows_to_be(1))
    browser.switch_to_window(browser.window_handles[0])
