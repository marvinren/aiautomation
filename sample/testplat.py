# coding=utf-8

import time
import pdb

from selenium import webdriver

browser = webdriver.Ie()
browser.get("http://10.12.1.30:28080/aialm")
time.sleep(0.5)

browser.find_element_by_id("UserAccount").send_keys("administrator")
browser.find_element_by_id("UserPwd").send_keys("AAbbcc123")

browser.find_element_by_id("loginIMG").click()
browser.find_element_by_id("loginIMG").click()
pdb.set_trace()
time.sleep(0.5)
# browser.execute_script(browser.find_element_by_id("loginIMG").get_attribute("onclick"))

time.sleep(2)

# browser.find_element_by_xpath("//em[text()='我的工作区']/parent::*").click()
# browser.find_element_by_xpath("//em[text()='需求查询']/parent::*").click()

browser.execute_script(browser.find_element_by_xpath("//em[text()='综合查询']/parent::li").get_attribute("onclick"))
browser.execute_script(browser.find_element_by_xpath("//a[text()='需求查询']").get_attribute("onclick"))


# browser.switch_to.default_content()
time.sleep(0.5)
browser.switch_to.frame("mainFrame")
browser.switch_to.frame(browser.find_element_by_tag_name("iframe"))

browser.execute_script(browser.find_element_by_xpath("//input[@value='需求查询']").get_attribute("onclick"))
pdb.set_trace()
