# coding: utf-8
# $$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$

# $$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$
# import
import time
from selenium.webdriver.chrome.webdriver import WebDriver


# 自作モジュール
from .utils import Logger
from .driverWait import Wait
from .browserHandler import BrowserHandler
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
        self.browser = BrowserHandler(debugMode=debugMode)
        self.fileRead = ResultFileRead(debugMode=debugMode)
        self.wait = Wait(debugMode=debugMode)

# ----------------------------------------------------------------------------------
# IDログイン

    def IDLogin(
        self,
        idBy: str, idValue: str, idText: str,
        passBy: str, passValue: str, passText: str,
        btnBy: str, btnValue: str, btnText: str,
        delay: int=2,
    ):

        # サイトを開いてCookieを追加
        self.openSite()
        time.sleep(delay)

        self.inputId(by=idBy, value=idValue, inputText=idText)
        time.sleep(delay)

        self.inputPass(by=passBy, value=passValue, inputText=passText)
        time.sleep(delay)

        self.clickLoginBtn(by=btnBy, value=btnValue, inputText=btnText)
        time.sleep(delay)

        return self.loginCheck()


# ----------------------------------------------------------------------------------
# TODO jsPageCheckerのデコ

    def openSite(self):
        self.browser.openSite()
        return self.chrome.get(self.url)


# ----------------------------------------------------------------------------------

    @property
    def currentUrl(self):
        return self.browser.currentUrl()


# ----------------------------------------------------------------------------------
# TODO jsPageCheckerのデコ
# IDの取得

    def inputId(self, by: str, value: str, inputText: str):
        return self.element.inputText(by=by, value=value, inputText=inputText)


# ----------------------------------------------------------------------------------
# TODO jsPageCheckerのデコ
# passの入力

    def inputPass(self, by: str, value: str, inputText: str):
        return self.element.inputText(by=by, value=value, inputText=inputText)


# ----------------------------------------------------------------------------------
# TODO jsPageCheckerのデコ
# ログインボタン押下

    def clickLoginBtn(self, by: str, value: str):
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
