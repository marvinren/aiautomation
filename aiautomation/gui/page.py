
class Page:

    def __init__(self, browser=None):
        self._browser = browser
        self._logger = self._browser.logger

    @property
    def browser(self):
        return self._browser

    @property
    def logger(self):
        return self._logger

    def switch_to_frame(self):
        pass
