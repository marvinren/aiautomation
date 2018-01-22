import time

from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.wait import WebDriverWait

from aiautomation.gui.page import Page


def input_tool(browser, name, input_text):
    """
    针对测试平台的输入框输入内容的工具方法
    :param browser:
    :param name:
    :param text:
    :return:
    """
    browser.find_element_by_xpath("//td[text()='%s：']/following-sibling::td[1]//input" % name).input(input_text)


def input_textarea_tool(browser, name, input_text):
    """
    参照input_tool(针对textarea)
    :param browser: 
    :param name: 
    :param input_text: 
    :return: 
    """
    browser.find_element_by_xpath("//td[text()='%s：']/following-sibling::td[1]//textarea" % name).input(input_text)


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


def calc_select(page, name, input_date):
    """
    针对测试平台的日期插件My97DatePicker进行选择
    :param input_date:
    :param page:
    :param name:
    :return:
    """
    if isinstance(page, Page):
        browser = page.browser
        if hasattr(page, 'switch_to_frame'):
            getattr(page, 'switch_to_frame')()
    else:
        browser = page
    date_array = input_date.split("-")
    year = date_array[0]
    month = date_array[1]
    day = date_array[2]
    browser.find_element_by_xpath("//td[text()='%s：']/following-sibling::td[1]//input" % name).click()
    browser.switch_to_frame(browser.find_element_by_xpath("//iframe[contains(@src, 'My97DatePicker.htm')]"))
    browser.execute_script("day_Click(%s, %s, %s)" % (year, month, day))
    if isinstance(page, Page):
        if hasattr(page, 'switch_to_frame'):
            getattr(page, 'switch_to_frame')()

def select_user(page, name, user_name):
    """
    选择人工具类
    :param browser:
    :param name:
    :param user_name:
    :return:
    """
    if isinstance(page, Page):
        browser = page.browser
    else:
        browser = page

    driver = browser.webdriver

    init_size = len(driver.window_handles)
    init_window = driver.current_window_handle
    if name is not None:
        browser.find_element_by_xpath("//td[starts-with(text(), '%s')]/parent::*//input[@type='button']" % name).click()
        WebDriverWait(browser.webdriver, 10).until(expected_conditions.number_of_windows_to_be(init_size + 1))
    else:
        time.sleep(0.5)

    browser.switch_to_windows_by_url("/SelectStaff")
    browser.find_element_by_id("searchPerson").input(user_name)
    browser.find_element_by_id("qryBtn").fire_event("onclick")

    time.sleep(1)
    WebDriverWait(browser.webdriver, 5).until(
        expected_conditions.text_to_be_present_in_element((By.ID, "DataTable_staffTable"), user_name))

    browser.find_element_by_xpath("//*[@id='DataTable_staffTable']//td[text()='%s']/parent::*" % user_name).click()
    time.sleep(0.5)
    browser.find_element_by_xpath("//input[@value='确认']").click()
    if name is not None:
        WebDriverWait(browser.webdriver, 3).until(expected_conditions.number_of_windows_to_be(init_size))
    else:
        WebDriverWait(browser.webdriver, 3).until(expected_conditions.number_of_windows_to_be(init_size - 1))
    browser.switch_to_window(init_window)
    time.sleep(0.5)
    if isinstance(page, Page):
        page.switch_to_frame()
