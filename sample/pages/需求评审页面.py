from aiautomation.gui.page import Page
from aiautomation.testcase.decorator import component


class 需求查询页面(Page):

    def switch_to_frame(self):
        pass

    @component("2000")
    def 录入评审信息(self, data=None):

        self.switch_to_frame()

        browser = self.browser
        