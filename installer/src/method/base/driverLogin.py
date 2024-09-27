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
import os
import pickle
import time
import requests
from datetime import datetime
from selenium.webdriver.chrome.webdriver import WebDriver


from selenium.common.exceptions import (NoSuchElementException,
                                        WebDriverException,
                                        TimeoutException)
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait

# 自作モジュール
from .utils import Logger
from .driverWait import Wait
from .fileRead import ResultFileRead


# $$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$
# **********************************************************************************


class Login:
    def __init__(self, chrome: WebDriver, loginUrl: str, url: str, debugMode=True):
        # logger
        self.getLogger = Logger(__name__, debugMode=debugMode)
        self.logger = self.getLogger.getLogger()

        self.chrome = chrome
        self.loginUrl = loginUrl
        self.url = url

        self.driverWait = Wait(chrome=self.chrome, debugMode=debugMode)
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


    def closeChrome(self):
        return self.chrome.quit()


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

    @property
    def session(self):
        # sessionを定義（セッションの箱を作ってるイメージ）
        return requests.Session()


# ----------------------------------------------------------------------------------


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


    def sessionLogin(self, cookies):
        session = self.sessionSetting(cookies=cookies)
        session.get(self.url)

        if not self.loginCheck():
            self.logger.error(f"セッションを使ったログインにも失敗しました:\n{cookies[30:]}")
            return None


# ----------------------------------------------------------------------------------

# Cookieを使ってログイン

    def cookieLogin(self):
        # pickleファイルの読込
        cookies = self.fileRead.readCookieLatestResult()

        # サイトを開いてCookieを追加
        self.openSite()
        for cookie in cookies:
            self.addCookie(cookie=cookie)

        # サイトをリロードしてCookieの適用を試行
        self.openSite()

        if not self.loginCheck():
            self.sessionLogin(cookies=cookies)
        return


# ----------------------------------------------------------------------------------
# 対象のサイトを開く

    def sever_open_site(self, url, by_pattern, check_path, notifyFunc, field_name):

        # サイトを開く前にurlを確認
        self.logger.debug(f"{field_name} url: {url}")
        self.logger.debug(f"{field_name} by_pattern: {by_pattern} , check_path: {check_path}")

        self.logger.info("対象のサイトを開く")

        time.sleep(2)

        self.chrome.get(url)
        current_url = self.chrome.current_url
        self.logger.debug(f"{field_name} URL: {current_url}")

        try:
            self.driver_wait._sever_element_clickable(by_pattern=by_pattern, element_path=check_path, notifyFunc=notifyFunc , field_name=field_name)

            self.logger.debug(f"{field_name}  入力準備 完了")

        except TimeoutException as e:
            self.logger.info(f"{field_name} 初回ロードに10秒以上かかってしまったためリロード: {e}")

            self.chrome.refresh()
            try:
                self.logger.debug(f"IDなどを入力 ができるかを確認")
                self.driver_wait._element_clickable(by_pattern=by_pattern, element_path=check_path, field_name=field_name)
                self.logger.debug(f"{field_name}  入力準備 完了")

            except TimeoutException as e:
                self.logger.info(f"{field_name} 2回目のロードエラーのためタイムアウト: {e}")


        except NoSuchElementException as e:
            self.logger.error(f" 要素が見つかりません: {by_pattern}: {check_path}, {e}")


        except WebDriverException as e:
            self.logger.error(f"{field_name} webdriverでのエラーが発生: {e}")


        except Exception as e:
            self.logger.error(f"{field_name} 処理中にエラーが発生: {e}")


        time.sleep(2)


# ----------------------------------------------------------------------------------
# サイトが複数あるケース
# titleとサイトが開いてるかどうかでサイトが開いてるかを確認

    def site_open_title_check(self, gss_url, gss_title, field_name, token, notifyFunc):
        try:
            self.logger.info(f"********** sites_open start **********")

            self.logger.debug(f"gss_url: {gss_url}")
            self.logger.debug(f"gss_title: {gss_title}")

            if gss_url:
                # サイトが開いてる確認してtitleが一致してるか確認
                self.driver_wait.js_and_title_check(
                    url=gss_url,
                    gss_title=gss_title,
                    field_name=field_name,
                    token=token,
                    notifyFunc=notifyFunc,
                )

            else:
                self.logger.error(f"gssからのデータを取得できません{gss_url}")
                raise

            self.logger.info(f"********** sites_open end **********")

        except Exception as e:
            self.logger.error(f"sites_open 処理中にエラーが発生:{e}")
            raise

# ----------------------------------------------------------------------------------
