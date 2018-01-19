#!/usr/bin/python3
# coding=utf-8
import abc
from aiautomation.testcase.browser import Browser


class ScenariosRecovery:
    """
    场景恢复的基类
    """
    __metaclass__ = abc.ABCMeta

    def __init__(self, logger, config):
        self._browser = None
        self._logger = logger
        self._config = config

    @abc.abstractmethod
    def recovery(self):
        """
        完成场景恢复的工作
        :return: 需要返回browser对象
        """
        pass
