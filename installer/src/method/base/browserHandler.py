# coding: utf-8
# $$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$

# $$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$
# import
from selenium.webdriver.chrome.webdriver import WebDriver


# 自作モジュール
from .utils import Logger


# $$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$
# **********************************************************************************


class BrowserHandler:
    def __init__(self, chrome: WebDriver, loginUrl: str, homeUrl: str, debugMode=True):
        # logger
        self.getLogger = Logger(__name__, debugMode=debugMode)
        self.logger = self.getLogger.getLogger()

        self.chrome = chrome
        self.homeUrl = homeUrl

# ----------------------------------------------------------------------------------


    def openSite(self):
        self.logger.debug(f"url: {self.url}")
        return self.chrome.get(self.url)


# ----------------------------------------------------------------------------------


    def currentUrl(self):
        return self.chrome.current_url()


# ----------------------------------------------------------------------------------


    def getCookies(self):
        return self.chrome.get_cookies()


# ----------------------------------------------------------------------------------


    def newOpenWindow(self):
        return self.chrome.execute_script("window.open('');")


# ----------------------------------------------------------------------------------


    def switchWindow(self):
        # 開いてるWindow数を確認
        if len(self.chrome.window_handles) > 1:
            self.chrome.switch_to.window(self.chrome.window_handles[1])
            self.chrome.get(self.url)
        else:
            self.logger.error("既存のWindowがないため、新しいWindowに切替ができません")


# ----------------------------------------------------------------------------------


    def addCookie(self, cookie):
        return self.chrome.add_cookie(cookie_dict=cookie)


# ----------------------------------------------------------------------------------
