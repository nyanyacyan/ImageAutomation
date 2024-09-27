# coding: utf-8
# $$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$

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

# $$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$
# **********************************************************************************


class Login:
    def __init__(self, chrome: WebDriver, url: str, debugMode=True):
        # logger
        self.getLogger = Logger(__name__, debugMode=debugMode)
        self.logger = self.getLogger.getLogger()

        self.chrome = chrome
        self.url = url
        self.driverWait = Wait(chrome=self.chrome, debugMode=debugMode)



# ----------------------------------------------------------------------------------


    def openSite(self):
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
# Cookieを使ってログイン

    def cookieLogin(self):
        # cookiesを初期化
        cookies = []

        # Cookieのフルパス
        pickle_file_path = self._get_full_path(file_name=file_name)

        # urlを事前確認
        self.logger.debug(f"{field_name}: main_url: {main_url}")

        # Cookieファイルを展開
        cookies = self._pickle_load(pickle_file_path=pickle_file_path, field_name=field_name)

        self.logger.debug(f"{field_name} cookies: {cookies}")

        self.chrome.get(main_url)

        for c in cookies:
            self.chrome.add_cookie(c)

        self.chrome.get(main_url)

        time.sleep(60)

        self.logger.info(f"{field_name}: Cookieを使ってメイン画面にアクセス")


        current_url = self.chrome.current_url
        self.logger.info(f"{field_name}: current_url: {current_url}")


        if main_url == current_url:
            self.logger.info(f"{field_name}: Cookieでのログイン成功")

        else:
            self.logger.warning("Cookieでのログイン失敗 sessionでのログインに変更")
            session = requests.Session()


            # セッションでのログイン
            # 項目はその時に応じて変更が必要
            cookie = cookies[0]
            session.cookies.set(
                name=cookie['name'],
                value=cookie['value'],
                domain=cookie['domain'],
                path=cookie['path'],
                # expires=cookie['expiry'],
                # secure=cookie['secure'],
                # rest={'HttpOnly': cookie['httpOnly'], 'SameSite': cookie['sameSite']}
            )

            self.logger.debug(f"name{cookie['name']},{cookie['value']},{cookie['domain']},{cookie['path']}")

            response = session.get(main_url)

            if main_url == self.chrome.current_url:
                self.logger.info(f"{field_name}: sessionでのログイン成功")

            else:
                self.logger.error(f"{field_name}: sessionでのログイン 失敗")
                raise

            # テキスト化
            res_text = response.text
            self.logger.debug(f"res_text: {res_text}"[:30])


        try:
            # ログインした後のページ読み込みの完了確認
            WebDriverWait(self.chrome, 5).until(
            lambda driver: driver.execute_script('return document.readyState') == 'complete'
            )
            self.logger.debug(f"{field_name}: ログインページ読み込み 完了")

        except Exception as e:
            self.logger.error(f"{field_name}: ログイン処理中 にエラーが発生: {e}")


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
