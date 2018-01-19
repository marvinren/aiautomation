from aiautomation.testcase.browser import Browser
from aiautomation.testcase.scenarios_recovery import ScenariosRecovery
import time

from aiautomation.utils.log import get_logger

class AialmRecovery(ScenariosRecovery):

    def recovery(self):
        self._logger.info("开始进入场景恢复")
        if self._browser is None or not self._browser.is_active():
            self._browser = Browser(browser_type="ie", logger=self._logger, config=self._config)
        time.sleep(1)
        # 查询是否登陆
        if not self._browser.title == "集团一级系统测试管理平台":
            self.login()
        else:
            self._browser.get("http://10.12.1.30:28080/aialm/webframe/shdesktopui/WebAppFrameSet_new.jsp")
        self._logger.info("场景回复结束")

        return self._browser

    def login(self):
        browser = self._browser
        browser.get("http://10.12.1.30:28080/aialm")
        browser.maximize_window()
        time.sleep(1)

        browser.find_element_by_id("UserAccount").send_keys("administrator")
        browser.find_element_by_id("UserPwd").send_keys("AAbbcc123")

        time.sleep(0.5)
        browser.find_element_by_id("loginIMG").click()
        time.sleep(1)
