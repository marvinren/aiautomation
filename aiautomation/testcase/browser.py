import time
from selenium import webdriver
from selenium.webdriver import DesiredCapabilities
from selenium.webdriver.remote.webdriver import WebDriver as RemoteWebDriver
from selenium.webdriver.support.wait import WebDriverWait

from aiautomation.testcase.decorator import step_log
from aiautomation.testcase.element import Element
from aiautomation.log.abstract_log import AbstractLog
from aiautomation.log.simple_log import SimpleLog


class Browser:
    """
    该类为webdriver（RemoteWebDriver）的委托类
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
            self.webdriver = webdriver.Ie(capabilities={'ignoreZoomSetting': True})
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
            config_implictly_wait = self.config.aiautomation.browser.implicitly_wait
            self.webdriver.implicitly_wait(config_implictly_wait)
        except Exception as e:
            self.webdriver.implicitly_wait(3)
            self.logger.warn("未配置aiautomation.browser.implicitly_wait，将使用默认值3s")
        try:
            config_page_load_timeout = self.config.aiautomation.browser.page_load_timeout
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

    @step_log(AbstractLog.STEP_TYPE_ELEMENT, __name__)
    def find_element_by_locate(self, locate):
        return self.find_element(locate[0], locate[1])

    #@step_log(AbstractLog.STEP_TYPE_ELEMENT, __name__)
    def switch_to_frame(self, frame_ref):
        ref = frame_ref
        if isinstance(ref, Element):
            ref = ref.web_element
        self.webdriver.switch_to.frame(ref)

    @property
    def windows_handles(self):
        return self.webdriver.window_handles

    @property
    def current_window_handle(self):
        return self.webdriver.current_window_handle

    def switch_to_windows_by_name(self, name):
        '''
        吐槽，简直就是狗屎方法，很不好用，一般人都不起名字
        :param name:
        :return:
        '''
        self.webdriver.switch_to.window(name)

    def switch_to_windows_by_url(self, contains_text):
        for window_id in self.webdriver.window_handles:
            self.webdriver.switch_to.window(window_id)
            url = self.webdriver.current_url
            if url.find(contains_text) >= 0:
                return
        raise ValueError("未找到适合的window")

    def get_waiter(self, timeout = 7):
        return WebDriverWait(self.webdriver, timeout)

    # @step_log(AbstractLog.STEP_TYPE_ELEMENT, __name__)
    # def find_element(self, by, value):
    #     ret = self.webdriver.find_element(by, value)
    #     element_delegate = Element(ret, self.logger, "%s:%s" % (by, value))
    #     return element_delegate
    #
    # @step_log(AbstractLog.STEP_TYPE_ELEMENT, __name__)
    # def find_elements(self, by, value):
    #     rets = self.webdriver.find_elements(by, value)
    #     element_delegates = list(map(lambda x: Element(x, self.logger, "%s:%s" % (by, value)), rets))
    #     return element_delegates

    @step_log(AbstractLog.STEP_TYPE_CHECK, __name__)
    def assert_check_point(self, check_point_name, expect_value, real_value, check_func):
        return check_func(expect_value, real_value)

    @step_log(AbstractLog.STEP_TYPE_CHECK, __name__)
    def assert_check_point_same(self, check_point_name, expect_value, real_value):
        return self.assert_check_point(check_point_name, expect_value, real_value, lambda x, y: x==y)

    @step_log(AbstractLog.STEP_TYPE_CHECK, __name__)
    def assert_check_point_true(self, check_point_name, result):
        return self.assert_check_point_same(check_point_name, True, result)

    def __getattr__(self, name):
        if hasattr(self.webdriver, name):
            #如果是查询多个元素要进行封装
            if name.startswith('find_elements'):
                def func(*key, **kwargs):
                    rets = getattr(self.webdriver, name)(*key, **kwargs)
                    element_delegates = list(map(lambda x: Element(x, self.logger, "%s" % str(key)), rets))
                    return element_delegates
                return func

            #如果是查询元素，要进行封装
            if name.startswith("find_element"):
                def func(*key, **kwargs):
                    ret = getattr(self.webdriver, name)(*key, **kwargs)
                    element_delegate = Element(ret, self.logger, "%s" % str(key))
                    return element_delegate
                return func

            return step_log(AbstractLog.STEP_TYPE_ELEMENT, __name__, self.logger)(getattr(self.webdriver, name))