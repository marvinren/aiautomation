
# 强制等待sleep wait
# 隐形等待
driver.implicitly_wait(30)
# 显示等待
from selenium.webdriver.support.ui import WebDriverWait

WebDriverWait(driver, 5).until(lambda s: s.execute_script("return jQuery.active == 0"))
# page_load
