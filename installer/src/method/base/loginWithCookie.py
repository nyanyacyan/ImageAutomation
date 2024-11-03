# coding: utf-8
# $$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$

# $$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$
# import
import requests, time
from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.common.exceptions import InvalidCookieDomainException

# 自作モジュール
from .utils import Logger
from .driverWait import Wait
from .seleniumBase import SeleniumBasicOperations
from .cookieManager import CookieManager
from .SQLite import SQLite
from .loginWithId import LoginID
from .driverDeco import jsCompleteWaitDeco
from .elementManager import ElementManager

decoInstance = jsCompleteWaitDeco(debugMode=True)


# $$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$
# **********************************************************************************


class CookieLogin:
    def __init__(self, chrome: WebDriver, loginUrl: str, homeUrl: str, signInUrl: str, debugMode=True):
        # logger
        self.getLogger = Logger(__name__, debugMode=debugMode)
        self.logger = self.getLogger.getLogger()

        self.chrome = chrome
        self.loginUrl = loginUrl
        self.homeUrl = homeUrl
        self.signInUrl = signInUrl

        # インスタンス
        self.browser = SeleniumBasicOperations(chrome=self.chrome, homeUrl=self.homeUrl, debugMode=debugMode)
        self.driverWait = Wait(chrome=self.chrome, debugMode=debugMode)
        self.cookieManager = CookieManager(chrome=self.chrome, loginUrl=self.loginUrl, homeUrl=self.homeUrl, debugMode=debugMode)
        self.idLogin = LoginID(chrome=self.chrome, homeUrl=self.homeUrl, loginUrl=self.loginUrl, debugMode=debugMode)
        self.sqLite = SQLite(debugMode=debugMode)
        self.element = ElementManager(chrome=self.chrome, debugMode=debugMode)

# ----------------------------------------------------------------------------------
# 2段階ログイン

    def flowSwitchLogin(self, cookies: dict, url: str, loginInfo: dict, delay: int = 1):
        if self.chrome.current_url == self.homeUrl:
            return

        if cookies is None:
            self.idLogin.flowLoginID(url=url, loginInfo=loginInfo)
            return

        if self.cookieLogin(cookies=cookies, url=url, loginInfo=loginInfo):
            time.sleep(delay)  # 広告などが遅れて表示されることを懸念
            # 検索画面、広告が合った場合に消去
            self.element.closePopup(by=loginInfo['modalBy'], value=loginInfo['modalValue'])
            self.logger.info(f"Cookieログインに成功")
        else:
            self.logger.error("Cookieログインに失敗したためセッションログインに切り替えます")
            if self.sessionLogin(cookies=cookies):
                self.logger.info(f"Cookieログインに成功")
            else:
                self.logger.error(f"セッションログインにも失敗: {cookies[30:]}")

        return


# ----------------------------------------------------------------------------------
# sessionログイン

    def sessionLogin(self, cookies):
        session = self.sessionSetting(cookies=cookies)
        session.get(self.url)
        return self.loginCheck()


# ----------------------------------------------------------------------------------
# Cookieログイン

    def cookieLogin(self, cookies: dict, url: str, loginInfo: dict):

        self.logger.info(f"cookies: {cookies}")

        # サイトを開いてCookieを追加
        self.openSite()

        if self.element.getElement(by=loginInfo['bypassIdBy'], value=loginInfo['bypassIdValue']):
            self.element.clickElement(by=loginInfo['bypassIdBy'], value=loginInfo['bypassIdValue'])

        try:
            self.addCookie(cookie=cookies)
            # サイトをリロードしてCookieの適用を試行
            self.openSite()

        except InvalidCookieDomainException as e:
            self.logger.error(f"ドメインが変わるサイトのためIDログインに切り替えます。{e}")
            self.idLogin.flowLoginID(url=url, loginInfo=loginInfo)

        return self.loginCheck(url=url)


# ----------------------------------------------------------------------------------


    def addCookie(self, cookie: dict):
        # クッキー情報をデバッグ
        self.logger.debug(f"Adding cookie: {cookie}")
        # 必須フィールドが揃っているか確認
        required_keys = ["name", "value"]
        for key in required_keys:
            if key not in cookie:
                self.logger.error(f"Cookie情報が入っていません: '{key}'")
                raise ValueError(f"Cookie情報が入っていません: '{key}'")

        # クッキーを追加
        return self.chrome.add_cookie(cookie_dict=cookie)


# ----------------------------------------------------------------------------------


    @decoInstance.jsCompleteWait
    def openSite(self):
        return self.browser.openSite()


# ----------------------------------------------------------------------------------


    @property
    def session(self):
        # sessionを定義（セッションの箱を作ってるイメージ）
        return requests.Session()


# ----------------------------------------------------------------------------------


    @decoInstance.jsCompleteWait
    def sessionSetting(self, cookies):
        if cookies:
            session = self.session
            cookie = cookies[0]
            session.cookies.set(
                name=cookie['name'],
                value=cookie['value'],
                domain=cookie['domain'],
                path=cookie['path'],
            )
            self.logger.debug(f"Cookieの中身:\nname{cookie['name']},{cookie['value']},{cookie['domain']},{cookie['path']}")
            return session
        else:
            self.logger.error(f"cookiesがありません")
            return None


# ----------------------------------------------------------------------------------


    def loginCheck(self, url: str):
        if url == self.chrome.current_url:
            self.logger.info(f"{__name__}: ログインに成功")
            return True
        else:
            self.logger.error(f"{__name__}: ログインに失敗")
            return False


# ----------------------------------------------------------------------------------
