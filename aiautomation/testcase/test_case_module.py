#!/usr/bin/python3
# coding=utf-8
import pymysql


class CaseInfo:

    def __init__(self, **kwargs):
        self._module_name = kwargs['module_name']
        self._module_id = kwargs['module_id']
        self._case_name = kwargs['case_name']
        self._case_id = kwargs['case_id']
        self._case_exec_id = kwargs['case_exec_id']
        self._parent_exec_id = kwargs['parent_exec_id']

    @property
    def module_name(self):
        return self._module_name

    @property
    def case_name(self):
        return self._case_name

    @property
    def case_id(self):
        return self._case_id

    @property
    def module_id(self):
        return self._module_id

    @property
    def case_exec_id(self):
        return self._case_exec_id

    @property
    def parent_exec_id(self):
        return self._parent_exec_id

    @case_exec_id.setter
    def case_exec_id(self, value):
        self._case_exec_id = value

    @parent_exec_id.setter
    def parent_exec_id(self, value):
        self._parent_exec_id = value


class TestCaseModule:

    @property
    def logger(self):
        return self._logger

    @property
    def config(self):
        return self._config

    @property
    def browser(self):
        return self._browser

    @property
    def case_info(self):
        return self.logger.testcase

    @browser.setter
    def browser(self, value):
        self._browser = value

    @case_info.setter
    def case_info(self, value):
        self._logger.testcase = value

    def __init__(self,
                 scenarios_recovery=None,
                 logger=None,
                 config=None,
                 browser=None
                 ):
        self._logger = logger
        self._scenarios_recovery = scenarios_recovery
        self._browser = browser
        self._config = config
        if self._logger and not hasattr(self._logger, "testcase"):
            self.logger.testcase = None

    def recovery(self):
        # 执行完场景回复才能进入
        self._browser = self._scenarios_recovery.recovery()

    def resume(self):
        config = self._config
        try:
            if config.aiautomation.runner.case_resume_close_browser == 'each':
                self._browser.close()
                self._browser.quit()
                self._browser = None
        except AttributeError:
            # 如果参数不存在不关闭浏览器
            self.logger.warn("未找到参数aiautomation.runner.case_resume_close_browser，默认不关闭浏览器")
        self.logger.testcase = None

    def create_page(self, page_class):
        return page_class(browser=self.browser)

