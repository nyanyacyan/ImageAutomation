# coding: utf-8
# $$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$

# $$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$
# import
from selenium.webdriver.chrome.webdriver import WebDriver


# 自作モジュール
from .utils import Logger


# $$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$
# **********************************************************************************


class CookieManager:
    def __init__(self, chrome: WebDriver, homeUrl: str, debugMode=True):
        # logger
        self.getLogger = Logger(__name__, debugMode=debugMode)
        self.logger = self.getLogger.getLogger()

        self.chrome = chrome
        self.homeUrl = homeUrl

# ----------------------------------------------------------------------------------

    @property
    def getCookies(self):
        return self.chrome.get_cookies()


# ----------------------------------------------------------------------------------


    @property
    def getCookie(self):
        cookies = self.getCookies
        return cookies[0]


# ----------------------------------------------------------------------------------
# Cookieの内容から有効期限を確認する

    def getCookieExpires(self):
        cookie = self.getCookie
        cookieName = cookie['name']
        cookieExpires = cookie.get['expires']
        cookieMaxAge = cookie.get['max-age']  # expiresよりも優先される

        if cookieMaxAge:
            self.logger.debug(f"Cookie {cookieName} の max-age を発見")
            return cookieMaxAge
        elif cookieExpires:
            self.logger.debug(f"Cookie {cookieName} の expires を発見")
            return cookieExpires
        else:
            self.logger.debug(f"Cookie {cookieName} には有効期限が設定されてません")
            return None


# ----------------------------------------------------------------------------------
# Cookieの内容をtextに保存する



# ----------------------------------------------------------------------------------
# Flow