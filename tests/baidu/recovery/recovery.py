import time

from aiautomation.testcase.browser import Browser
from aiautomation.testcase.scenarios_recovery import ScenariosRecovery


class BaiduRecovery(ScenariosRecovery):
    def recovery(self):
        browser = Browser(browser_type="chrome", logger=self._logger, config=self._config)
        browser.get("http://www.baidu.com")
        # browser.maximize_window()
        time.sleep(1)

        return browser
