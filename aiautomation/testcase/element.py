from selenium.webdriver.remote.webelement import WebElement


class Element(WebElement):
    """
    WebElement的委托类
    """

    def __init__(self, web_element, logger=None, name=None):
        self.web_element = web_element
        self.logger = logger
        self.name = name

    # === 新增方法 ====
    def input(self, *value):
        self.clear()
        self.web_element.send_keys(*value)
        self.logger.element_log(self.logger.testcase.case_id,
                                self.logger.testcase.case_exec_id,
                                self.logger.testcase.node_id, self.name, "输入内容")

    def fire_event(self, event_name):
        self.web_element.parent.execute_script(
            "if(arguments[0].fireEvent) "
            "{ arguments[0].fireEvent('%s'); }" 
            "else"
            "{ arguments[0].%s();}" % (event_name, event_name)
            , self.web_element)
        self.logger.element_log(self.logger.testcase.case_id,
                                self.logger.testcase.case_exec_id,
                                self.logger.testcase.node_id, self.name, "触发事件:%s" % event_name)

    # === 原方法 ===
    def send_keys(self, *value):
        self.web_element.send_keys(*value)
        self.logger.element_log(self.logger.testcase.case_id,
                                self.logger.testcase.case_exec_id,
                                self.logger.testcase.node_id, self.name, "输入内容send_keys")

    def click(self):
        self.web_element.click()
        self.logger.element_log(self.logger.testcase.case_id,
                                self.logger.testcase.case_exec_id,
                                self.logger.testcase.node_id, self.name, "单击")

    def __getattr__(self, item):
        if hasattr(self.web_element, item):
            return getattr(self.web_element, item)
        else:
            raise ValueError("Can't found the %s method/attribute." % item)
