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
from .driverDeco import jsCompleteWaitDeco

decoInstance = jsCompleteWaitDeco(debugMode=True)


# $$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$
# **********************************************************************************


class LoginID:
    def __init__(self, chrome: WebDriver, loginUrl: str, homeUrl: str, debugMode=True):
        # logger
        self.getLogger = Logger(__name__, debugMode=debugMode)
        self.logger = self.getLogger.getLogger()

        self.chrome = chrome
        self.loginUrl = loginUrl
        self.homeUrl = homeUrl

        # インスタンス
        self.element = ElementManager(chrome=chrome, debugMode=debugMode)
        self.browser = BrowserHandler(chrome=chrome, homeUrl=self.homeUrl, debugMode=debugMode)


# ----------------------------------------------------------------------------------
# IDログイン
# loginInfoはconstから取得
    @decoInstance.jsCompleteWaitRetry()
    def loginID(self, loginInfo: dict, delay: int=2):

        # サイトを開いてCookieを追加
        self.openSite()
        time.sleep(delay)

        self.inputId(by=loginInfo['idBy'], value=loginInfo['idValue'], inputText=loginInfo['idText'])
        time.sleep(delay)

        self.inputPass(by=loginInfo['passBy'], value=loginInfo['passValue'], inputText=loginInfo['passText'])
        time.sleep(delay)

        self.clickLoginBtn(by=loginInfo['btnBy'], value=loginInfo['btnValue'], inputText=loginInfo['btnText'])
        time.sleep(delay)

        return self.loginCheck()


# ----------------------------------------------------------------------------------


    @decoInstance.jsCompleteWait()
    def openSite(self):
        return self.chrome.get(self.loginUrl)


# ----------------------------------------------------------------------------------

    @property
    def currentUrl(self):
        return self.browser.currentUrl()


# ----------------------------------------------------------------------------------
# IDの取得

    def inputId(self, by: str, value: str, inputText: str):
        return self.element.inputText(by=by, value=value, inputText=inputText)


# ----------------------------------------------------------------------------------
# passの入力


    def inputPass(self, by: str, value: str, inputText: str):
        return self.element.inputText(by=by, value=value, inputText=inputText)


# ----------------------------------------------------------------------------------
# ログインボタン押下

    @decoInstance.jsCompleteWait
    def clickLoginBtn(self, by: str, value: str):
        return self.element.clickElement(by=by, value=value)


# ----------------------------------------------------------------------------------


    def loginCheck(self):
        if self.homeUrl == self.currentUrl:
            self.logger.info(f"{__name__}: ログインに成功")
            return True
        else:
            self.logger.error(f"{__name__}: ログインに失敗")
            return False


# ----------------------------------------------------------------------------------
