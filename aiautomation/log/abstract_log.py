#!/usr/bin/python3
# coding=utf-8

import abc

from aiautomation.testcase.test_case_module import CaseInfo
from aiautomation.testcase.test_plan import PlanInfo
from aiautomation.utils.log import get_logger


class AbstractLog:
    """
        该类为执行日志的基类，可以根据不同需要实现不同的的日志记录类实现相关方法
    """
    __metaclass__ = abc.ABCMeta

    STEP_TYPE_STEP = "STEP"
    STEP_TYPE_COMPONENT = "COMPONENT"
    STEP_TYPE_ELEMENT = "ELEMENT"
    STEP_TYPE_CHECK = "CHECK"

    START_STATUS = 0
    SUCCESS_STATUS = 10
    ERROR_STATUS = 11

    def __init__(self, config=None):
        self._test_plan = None
        self._test_case = None
        self._config = config
        self.log = get_logger(__name__)

    @property
    def testcase(self):
        return self._test_case

    @testcase.setter
    def testcase(self, value):
        if value is not None and not isinstance(value, CaseInfo):
            raise ValueError("%s日志类的计划属性，需要是CaseInfo类型" % __name__)
        self._test_case = value

    @property
    def testplan(self):
        return self._test_plan

    @testplan.setter
    def testplan(self, value):
        if value is not None and not isinstance(value, PlanInfo):
            raise ValueError("%s日志类的计划属性，需要是TestPlan类型" % __name__)
        self._test_plan = value

    def get_logger(self, name: object) -> object:
        self.log = get_logger(name)
        return self.log

    def info(self, msg, *keys, **kwargs):
        self.log.info(msg)

    def debug(self, msg, *keys, **kwargs):
        self.log.debug(msg)

    def warn(self, msg, *keys, **kwargs):
        self.log.warn(msg)

    def error(self, msg, *keys, **kwargs):
        self.log.error(msg)

    @abc.abstractmethod
    def step_log_before(self, oper_type, oper_name, oper_id, parent_oper_id = None, *key, **kwargs):
        pass

    @abc.abstractmethod
    def step_log_after(self, oper_type, oper_name, oper_id, oper_time, result, log_content, parent_oper_id = None, *key, **kwargs):
        pass

    @abc.abstractmethod
    def case_log_before(self, *key, **kwargs):
        pass

    @abc.abstractmethod
    def case_log_after(self, result, run_time, log_content, *key, **kwargs):
        pass

    @abc.abstractmethod
    def plan_log_before(self, *key, **kwargs):
        pass

    @abc.abstractmethod
    def plan_log_after(self, *key, **kwargs):
        pass