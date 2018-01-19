# coding=utf-8


from selenium import webdriver
import time

from selenium.webdriver import ActionChains

browser = webdriver.Ie()
#webdriver.Chrome()

url = 'http://www.baidu.com'

# 通过get方法获取当前URL打印
print("now access %s" % (url))
browser.get(url)

time.sleep(2)
e = browser.find_element_by_xpath("//a[text()='hao123']")
e.click()
e.click()
print(e.get_attribute("outerHTML"))
ActionChains(browser).move_to_element(e).click(e).perform()

time.sleep(2)
browser.find_element_by_id("kw").send_keys("selenium")
browser.find_element_by_id("su").click()
browser.find_element_by_xpath("//a[text()='百度首页']").click()
time.sleep(3)
browser.quit()
