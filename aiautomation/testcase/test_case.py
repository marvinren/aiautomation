#!/usr/bin/python3
# coding=utf-8


class CaseInfo:

    def __init__(self, module_name, case_name, case_id, case_exec_id, node_id):
        self._module_name = module_name
        self._case_name = case_name
        self._case_id = case_id
        self._case_exec_id = case_exec_id
        self._node_id = node_id

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
    def case_exec_id(self):
        return self._case_exec_id

    @property
    def node_id(self):
        return self._node_id


class TestCase:

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
        config = self._config.getConfig()
        try:
            if config.aiautomation.runner.case_resume_close_browser == 'each':
                self._browser.close()
                self._browser.quit()
                self._browser = None
        except AttributeError:
            # 如果参数不存在不关闭浏览器
            self.logger.warn("未找到参数aiautomation.runner.case_resume_close_browser，默认不关闭浏览器")
        self.logger.testcase = None

