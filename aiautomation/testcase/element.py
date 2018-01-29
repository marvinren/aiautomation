from functools import wraps
from types import MethodType

from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement

from aiautomation.log.abstract_log import AbstractLog
from aiautomation.testcase.decorator import step_log


class Element(WebElement):
    """
    WebElement的委托类
    """

    def __init__(self, web_element, logger=None, name=None):
        self.web_element = web_element
        # self._parent = web_element.parent
        # self._id = web_element.id
        self.logger = logger
        self.name = name

    def find_element(self, by=By.ID, value=None):
        """
        把查询结果用Elment代替
        :param by:
        :param value:
        :return:
        """
        ret = self.web_element.find_element(by, value)
        return Element(ret, self.logger)

    def find_elements(self, by=By.ID, value=None):
        """
        把查询结果用Elment代替
        :param by:
        :param value:
        :return:
        """
        rets = self.web_element.find_elements(by, value)
        return list(map(lambda e: Element(e, self.logger), rets))

    @step_log(AbstractLog.STEP_TYPE_ELEMENT, __name__)
    def input(self, *value):
        self.web_element.clear()
        self.web_element.send_keys(*value)

    @step_log(AbstractLog.STEP_TYPE_ELEMENT, __name__)
    def dbl_click(self):
        """
        双击方法的封装
        :return:
        """
        ActionChains(self.parent).move_to_element(self.web_element).double_click(self.web_element).perform()

    @step_log(AbstractLog.STEP_TYPE_ELEMENT, __name__)
    def fire_event(self, event_name):
        self.web_element.parent.execute_script(
            "if(arguments[0].fireEvent) "
            "{ arguments[0].fireEvent('%s'); }"
            "else"
            "{ arguments[0].%s();}" % (event_name, event_name)
            , self.web_element)

    @step_log(AbstractLog.STEP_TYPE_ELEMENT, __name__)
    def select(self, text):
        self.web_element.find_element_by_xpath("//option[text()='%s']" % text).click()

    def __getattribute__(self, name):
        if name == "web_element" or name.startswith("find_element"):
            return object.__getattribute__(self, name)

        if hasattr(self.web_element, name):
            if not callable(getattr(self.web_element, name)):
                return getattr(self.web_element, name)
            else:
                return step_log(AbstractLog.STEP_TYPE_ELEMENT, __name__, self.logger)(getattr(self.web_element, name))

        return object.__getattribute__(self, name)
