# coding: utf-8
# $$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$

# $$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$
# import
from selenium.webdriver.chrome.webdriver import WebDriver


# 自作モジュール
from .utils import Logger


# $$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$
# **********************************************************************************


class SeleniumBasicOperations:
    def __init__(self, chrome: WebDriver, homeUrl: str, debugMode=True):
        # logger
        self.getLogger = Logger(__name__, debugMode=debugMode)
        self.logger = self.getLogger.getLogger()

        self.chrome = chrome
        self.homeUrl = homeUrl

# ----------------------------------------------------------------------------------


    def openSite(self):
        self.logger.debug(f"url: {self.homeUrl}")
        return self.chrome.get(url=self.homeUrl)


# ----------------------------------------------------------------------------------


    def currentUrl(self):
        return self.chrome.current_url()


# ----------------------------------------------------------------------------------


    def newOpenWindow(self):
        return self.chrome.execute_script("window.open('');")


# ----------------------------------------------------------------------------------


    def switchWindow(self):
        # 開いてるWindow数を確認
        if len(self.chrome.window_handles) > 1:
            self.chrome.switch_to.window(self.chrome.window_handles[1])
            self.chrome.get(self.homeUrl)
        else:
            self.logger.error("既存のWindowがないため、新しいWindowに切替ができません")


# ----------------------------------------------------------------------------------
