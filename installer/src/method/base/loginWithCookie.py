# coding: utf-8
# $$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$

# TODO 最新のCookieテキストを確認→問題なければCookieログイン
# TODO 問題なければこれでログイン
# TODO 問題会った場合には
# TODO ログイン画面にアクセス
# TODO IDとパスを入力してログイン
# TODO Cookieの取得
# TODO Cookieログイン



# $$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$
# import
import requests
from selenium.webdriver.chrome.webdriver import WebDriver


# 自作モジュール
from .utils import Logger
from .driverWait import Wait
from .browserHandler import BrowserHandler


# $$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$
# **********************************************************************************


class CookieLogin:
    def __init__(self, chrome: WebDriver, loginUrl: str, homeUrl: str, debugMode=True):
        # logger
        self.getLogger = Logger(__name__, debugMode=debugMode)
        self.logger = self.getLogger.getLogger()

        self.chrome = chrome
        self.url = homeUrl

        # インスタンス
        self.browser = BrowserHandler(debugMode=debugMode)
        self.driverWait = Wait(chrome=self.chrome, debugMode=debugMode)


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
        return


# ----------------------------------------------------------------------------------
# sessionログイン

    def sessionLogin(self, cookies):
        session = self.sessionSetting(cookies=cookies)
        session.get(self.url)
        return self.loginCheck()


# ----------------------------------------------------------------------------------
# Cookieログイン

    def cookieLogin(self, cookies):

        # サイトを開いてCookieを追加
        self.openSite()
        for cookie in cookies:
            self.addCookie(cookie=cookie)

        # サイトをリロードしてCookieの適用を試行
        self.openSite()

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

    @property
    def session(self):
        # sessionを定義（セッションの箱を作ってるイメージ）
        return requests.Session()


# ----------------------------------------------------------------------------------
# TODO jsPageCheckerのデコ


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


    def loginCheck(self):
        if self.url == self.currentUrl:
            self.logger.info(f"{__name__}: ログインに成功")
            return True
        else:
            self.logger.error(f"{__name__}: ログインに失敗")
            return False


# ----------------------------------------------------------------------------------
