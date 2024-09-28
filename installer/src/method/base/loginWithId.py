# coding: utf-8
# $$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$

# $$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$
# import
import time
from selenium.webdriver.chrome.webdriver import WebDriver


# 自作モジュール
from .utils import Logger
from .driverWait import Wait
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
        self.wait = Wait(debugMode=debugMode)

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

    def inputId(self, by: str, value: str, inputText: str):
        return self.element.inputText(by=by, value=value, inputText=inputText)


# ----------------------------------------------------------------------------------
# passの入力

    def inputPass(self, by: str, value: str, inputText: str):
        return self.element.inputText(by=by, value=value, inputText=inputText)


# ----------------------------------------------------------------------------------
# ログインボタン押下

    def clickLoginBtn(self, by: str, value: str):
        return self.element.clickElement(by=by, value=value)


# ----------------------------------------------------------------------------------


    def loginBtnCheck(self):
        if self.wait.jsPageChecker():
            self.logger.info(f"{__name__}: ログインに成功")
            return True
        else:
            self.logger.error(f"{__name__}: ログインに失敗")
            return False


# ----------------------------------------------------------------------------------
# IDログイン

    def IDLogin(
        self,
        idBy: str,
        idValue: str,
        idText: str,
        passBy: str,
        passValue: str,
        passText: str,
        delay: int=2,
    ):

        # サイトを開いてCookieを追加
        self.openSite()
        time.sleep(delay)

        self.inputId(by=idBy, value=idValue, inputText=idText)
        time.sleep(delay)

        self.inputPass(by=passBy, value=passValue, inputText=passText)
        time.sleep(delay)

        return self.clickLoginBtn()


# ----------------------------------------------------------------------------------
# 2段階ログイン

    def (self):



# ----------------------------------------------------------------------------------
