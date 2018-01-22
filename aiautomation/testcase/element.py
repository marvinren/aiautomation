from functools import wraps
from types import MethodType

from selenium.webdriver.remote.webelement import WebElement

from aiautomation.log.abstract_log import AbstractLog
from aiautomation.testcase.decorator import step_log


class Element:
    """
    WebElement的委托类
    """

    def __init__(self, web_element, logger=None, name=None):
        self.web_element = web_element
        # self._parent = web_element.parent
        # self._id = web_element.id
        self.logger = logger
        self.name = name

    @property
    def text(self):
        return self.web_element.text

    @step_log(AbstractLog.STEP_TYPE_ELEMENT, __name__)
    def input(self, *value):
        self.web_element.clear()
        self.web_element.send_keys(*value)

    @step_log(AbstractLog.STEP_TYPE_ELEMENT, __name__)
    def fire_event(self, event_name):
        self.web_element.parent.execute_script(
            "if(arguments[0].fireEvent) "
            "{ arguments[0].fireEvent('%s'); }"
            "else"
            "{ arguments[0].%s();}" % (event_name, event_name)
            , self.web_element)

    @step_log(AbstractLog.STEP_TYPE_ELEMENT, __name__)
    def find_element(self, by, value):
        ret = self.web_element.find_element(by, value)
        element_delegate = Element(ret, self.logger, "%s:%s" % (by, value))
        return element_delegate

    @step_log(AbstractLog.STEP_TYPE_ELEMENT, __name__)
    def find_elements(self, by, value):
        rets = self.web_element.find_elements(by, value)
        element_delegates = list(map(lambda x: Element(x, self.logger, "%s:%s" % (by, value)), rets))
        return element_delegates

    @step_log(AbstractLog.STEP_TYPE_ELEMENT, __name__)
    def select(self, text):
        self.web_element.find_element_by_xpath("//option[text()='%s']" % text).click()

    def __getattr__(self, item):
        if hasattr(self.web_element, item):
            return step_log(AbstractLog.STEP_TYPE_ELEMENT, __name__, self.logger)(getattr(self.web_element, item))

        else:
            raise ValueError("Can't found the %s method/attribute." % item)
