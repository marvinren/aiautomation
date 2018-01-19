import time
from selenium import webdriver
from selenium.webdriver.remote.webdriver import WebDriver as RemoteWebDriver
from aiautomation.testcase.element import Element
from aiautomation.log.abstract_log import AbstractLog
from aiautomation.log.simple_log import SimpleLog


class Browser(RemoteWebDriver):
    """
    该类为webdriver的委托类
    """

    def __init__(self, logger=None, config=None, browser_type="chrome", *key, **kwargs):
        """
        创建时候需要传入type类型，主要为:ie, chrome, firefox, edge，默认使用chrome
        Usage: browser = Browser("ie")
        :param logger: 日志记录类
        :param browser_type: 使用的浏览器类型
        :param key:
        :param kwargs:
        """

        self.logger = logger
        self.config = config

        if browser_type == "ie":
            self.webdriver = webdriver.Ie(*key, **kwargs)
        elif browser_type == "chrome":
            self.webdriver = webdriver.Chrome(*key, **kwargs)
        elif browser_type == "firefox":
            self.webdriver = webdriver.Firefox(*key, **kwargs)
        elif browser_type == "edge":
            self.webdriver = webdriver.Edge(*key, **kwargs)
        else:
            self.webdriver = webdriver.Chrome(*key, **kwargs)

        # 隐式等待时间设置
        try:
            config_implictly_wait = self.config.getConfig().aiautomation.browser.implicitly_wait
            self.webdriver.implicitly_wait(config_implictly_wait)
        except Exception as e:
            self.webdriver.implicitly_wait(3)
            self.logger.warn("未配置aiautomation.browser.implicitly_wait，将使用默认值3s")
        try:
            config_page_load_timeout = self.config.getConfig().aiautomation.browser.page_load_timeout
            self.webdriver.set_page_load_timeout(config_page_load_timeout)
        except:
            self.webdriver.set_page_load_timeout(7)
            self.logger.warn("未配置aiautomation.browser.page_load_timeout，将使用默认值7s")

    def is_active(self):
        try:
            # 如果无法取得title说明浏览器已经死掉或者关闭
            self.webdriver.title
            len(self.webdriver.window_handles) > 0
        except:
            return False
        return True

    def find_element(self, by, value):
        ret = self.webdriver.find_element(by, value)
        element_delegate = Element(ret, self.logger, "%s:%s" % (by, value))
        case_info = self.logger.testcase
        self.logger.element_log(case_info.case_id, case_info.case_exec_id, case_info.node_id, "%s:%s" % (by, value),
                                "查找控件find_element")

        return element_delegate

    def find_elements(self, by, value):
        rets = self.webdriver.find_elements(by, value)
        element_delegates = list(map(lambda x: Element(x, self.logger, "%s:%s" % (by, value)), rets))
        case_info = self.logger.testcase
        self.logger.element_log(case_info.case_id, case_info.case_exec_id, case_info.node_id, "%s:%s" % (by, value),
                                "查找多个控件find_elements")
        return element_delegates

    def get(self, url):
        self.webdriver.get(url)
        case_info = self.logger.testcase
        self.logger.element_log(case_info.case_id, case_info.case_exec_id, case_info.node_id, "浏览器",
                                "浏览器跳转url：%s" % url)

    def switch_to_frame(self, frame_ref):
        self.webdriver.switch_to_frame(frame_ref)
        case_info = self.logger.testcase
        self.logger.element_log(case_info.case_id, case_info.case_exec_id, case_info.node_id, "Frame",
                                "Frame跳转：%s" % frame_ref.name)

    def switch_to_default_content(self):
        self.webdriver.switch_to_default_content()
        case_info = self.logger.testcase
        self.logger.element_log(case_info.case_id, case_info.case_exec_id, case_info.node_id, "Frame",
                                "Frame跳转到默认")

    def __getattr__(self, name):
        if hasattr(self.webdriver, name):
            return getattr(self.webdriver, name)
        #
        # def _missing(*args, **kwargs):
        #     print("A missing method was called.")
        #     print("The object was %r, the method was %r. " % (self, name))
        #     print("It was called with %r and %r as arguments" % (args, kwargs))
        #     raise ValueError("the missing method has been called.")
        #
        # return _missing
