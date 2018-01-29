import time

from aiautomation.testcase.browser import Browser
from aiautomation.testcase.scenarios_recovery import ScenariosRecovery


class 测试平台场景恢复(ScenariosRecovery):

    def recovery(self):
        self._logger.info("开始进入场景恢复")
        if self._browser is None or not self._browser.is_active():
            self._browser = Browser(browser_type="ie", logger=self._logger, config=self._config)
        time.sleep(1)
        self._logger.info("场景已恢复")

        return self._browser
