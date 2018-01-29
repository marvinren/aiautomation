# coding: utf-8
import time
from selenium.webdriver.common.by import By

from aiautomation.gui.page import Page
from aiautomation.testcase.decorator import component


class 空组件(Page):

    @component(11)
    def 空组件(self, data=None):
        print("空组件")


