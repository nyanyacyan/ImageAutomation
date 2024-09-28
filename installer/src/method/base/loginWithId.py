# coding: utf-8
# $$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$

# $$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$
# import
import requests
from selenium.webdriver.chrome.webdriver import WebDriver


# 自作モジュール
from .utils import Logger
from .elementManager import ElementManager
from .fileRead import ResultFileRead


# $$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$
# **********************************************************************************


class IdLogin:
    def __init__(self, chrome: WebDriver, loginUrl: str, url: str, debugMode=True):
        # logger
        self.getLogger = Logger(__name__, debugMode=debugMode)
        self.logger = self.getLogger.getLogger()

        self.chrome = chrome
        self.loginUrl = loginUrl
        self.url = url

        self.element = ElementManager(debugMode=debugMode)
        self.fileRead = ResultFileRead(debugMode=debugMode)


# ----------------------------------------------------------------------------------


    def openSite(self):
        self.logger.debug(f"url: {self.url}")
        return self.chrome.get(self.url)


# ----------------------------------------------------------------------------------

    @property
    def getCookies(self):
        return self.chrome.get_cookies()


# ----------------------------------------------------------------------------------

    @property
    def currentUrl(self):
        return self.chrome.current_url


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
# IDの取得

    def getInputId(self, by: str, value: str, inputText: str):
        return self.element.inputText(by=by, value=value, inputText=inputText)


# ----------------------------------------------------------------------------------
# passの入力

    def getInputPass(self, by: str, value: str, inputText: str):
        return self.element.inputText(by=by, value=value, inputText=inputText)


# ----------------------------------------------------------------------------------
# ログインボタン押下

    def getLoginBtn(self, by: str, value: str):
        return self.element.clickElement(by=by, value=value)


# ----------------------------------------------------------------------------------


    def loginCheck(self):
        if self.url == self.currentUrl:
            self.logger.info(f"{__name__}: ログインに成功")
            return True
        else:
            self.logger.error(f"{__name__}: ログインに失敗")
            return False


# ----------------------------------------------------------------------------------
# sessionログイン

    def sessionLogin(self, cookies):
        session = self.sessionSetting(cookies=cookies)
        session.get(self.url)

        return self.loginCheck()


# ----------------------------------------------------------------------------------
# Cookieログイン

    def cookieLogin(self):

        # サイトを開いてCookieを追加
        self.openSite()


        return self.loginCheck()


# ----------------------------------------------------------------------------------
# 2段階ログイン

    def switchLogin(self):
        # pickleファイルの読込
        cookies = self.fileRead.readCookieLatestResult()

        if self.cookieLogin(cookies=cookies):
            self.logger.info(f"Cookieログインに成功")
        else:
            self.logger.error("Cookieログインに失敗したためセッションログインに切り替えます")
            if self.sessionLogin(cookies=cookies):
                self.logger.info(f"Cookieログインに成功")
            else:
                self.logger.error(f"セッションログインにも失敗: {cookies[30:]}")
        return None


# ----------------------------------------------------------------------------------
