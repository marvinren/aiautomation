#!/usr/bin/python3
# coding=utf-8

import abc

from aiautomation.utils.log import get_logger


class AbstractLog:
    """
        该类为执行日志的基类，可以根据不同需要实现不同的的日志记录类实现相关方法
    """
    __metaclass__ = abc.ABCMeta

    STEP_TYPE_STEP = "STEP"
    STEP_TYPE_COMPONENT = "COMPONENT"
    STEP_TYPE_DATA = "DATA"
    STEP_TYPE_ELEMENT = "ELEMENT"
    STEP_TYPE_OTHER = "OTHER"

    def __init__(self):
        self._exec_plan = None
        self._test_case = None
        self.log = get_logger(__name__)

    @property
    def testcase(self):
        return self._test_case

    @testcase.setter
    def testcase(self, value):
        self._test_case = value

    @property
    def execplan(self):
        return self._exec_plan

    @execplan.setter
    def execplan(self, value):
        self._exec_plan = value

    def get_logger(self, name):
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
    def before_step_log(self, oper_type, oper_name, case_id, case_exec_id, node_id, component_id, *key, **kwargs):
        """
        在步骤（控件基本操作，获取数据，组件等）前执行，记录日志
        :param oper_type:
        :param oper_name:
        :param case_id:
        :param case_exec_id:
        :param node_id:
        :param component_id:
        :return:
        """
        pass

    @abc.abstractmethod
    def after_step_log(self, oper_type, oper_name, case_id, case_exec_id, node_id, component_id, oper_time, result, log_content, *key, **kwargs):
        """
        在步骤（控件基本操作，获取数据，组件等）后执行，记录日志
        :param log_content:
        :param oper_type:
        :param oper_name:
        :param case_id:
        :param case_exec_id:
        :param node_id:
        :param component_id:
        :param oper_time:
        :param result:
        :return:
        """
        pass

    @abc.abstractmethod
    def before_case_log(self, case_id, case_exec_id,  node_id, case_name, module_name, *key, **kwargs):
        """
        在案例执行前记录日志
        :param node_id:
        :param case_id:
        :param case_exec_id:
        :param case_name:
        :param module_name:
        :return:
        """
        pass

    @abc.abstractmethod
    def after_case_log(self, case_id, case_exec_id,  node_id, case_name, module_name, result, run_time, log_content, *key, **kwargs):
        """
        在案例执行后记录日志
        :param node_id:
        :param case_id:
        :param case_exec_id:
        :param case_name:
        :param module_name:
        :param result:
        :param run_time:
        :param log_content:
        :return:
        """
        pass

    @abc.abstractmethod
    def element_log(self, case_id, case_exec_id, node_id, element, action):
        """
        记录空间操作
        :param case_id:
        :param case_exec_id:
        :param node_id:
        :param element:
        :param action:
        :return:
        """
        pass