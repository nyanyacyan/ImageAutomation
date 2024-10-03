# coding: utf-8
# $$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$

# $$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$
# import

import requests
import os
import time
from datetime import datetime
from bs4 import BeautifulSoup
from functools import wraps
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import TimeoutException

# 自作モジュール
from .utils import Logger



# $$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$
# **********************************************************************************


class Wait:
    def __init__(self, chrome, debugMode=True):
        self.chrome = chrome

        # logger
        self.getLogger = Logger(__name__, debugMode=debugMode)
        self.logger = self.getLogger.getLogger()


# ----------------------------------------------------------------------------------


# ロケーター選択→直接文字列で入れ込むことができない

    def _locator_select(self, locator):
        mapping = {
            'ID' : By.ID,
            'XPATH' : By.XPATH,
            'CLASS' : By.CLASS_NAME,
            'CSS' : By.CSS_SELECTOR,
            'TAG' : By.TAG_NAME,
            'NAME' : By.NAME,
            'LINK_TEXT': By.LINK_TEXT,  # リンクテキスト全体に一致する要素を見つける
            'PARTIAL_LINK_TEXT': By.PARTIAL_LINK_TEXT  # リンクテキストの一部に一致する要素を見つける
        }

        # 入力された文字を大文字に直して選択
        return mapping.get(locator.upper())


# ----------------------------------------------------------------------------------
# # URLが変わるまで待機 デフォルト10秒
# self.driver_wait._url_change(current_url=, timeout=)

    def _url_change(self, current_url, field_name, timeout: int=10):
        try:
            WebDriverWait(self.chrome, timeout).until(EC.url_changes(current_url))
            self.logger.debug(f"{field_name} URLの切り替え成功")

        except TimeoutException as e:
            self.logger.error(f"{field_name} URLの切り替えされるまで、{timeout}秒以上経過したためタイムアウト: {e}")
            raise

        except Exception as e:
            self.logger.error(f"{field_name} URLの切り替えの待機中になんらかのエラーが発生 {e}")
            raise


# ----------------------------------------------------------------------------------
# クリックができるようになるまで待機 デフォルト10秒
# self.driver_wait._element_clickable(by_pattern=, xpath=, timeout=)

    def _element_clickable(self, by_pattern, element_path, field_name, timeout=10):
        try:
            WebDriverWait(self.chrome, timeout).until(EC.element_to_be_clickable((self._locator_select(by_pattern), element_path)))
            self.logger.debug(f"{field_name} クリックできる状態")

        except TimeoutException as e:
            self.logger.error(f"{field_name} クリックが可能になるまで、{timeout}秒以上経過したためタイムアウト: {e}")


        except Exception as e:
            self.logger.error(f"{field_name} クリックが可能になるまでの待機中になんらかのエラーが発生: {e}")



# ----------------------------------------------------------------------------------
#* locatorなし→変数による代入（事前に要素を選択して変数代入してあるものを選択）
# self.driver_wait._no_locator_clickable(variable_name=, field_name=, timeout=)

    def _no_locator_clickable(self, variable_name, field_name, timeout=10):
        try:
            WebDriverWait(self.chrome, timeout).until(EC.element_to_be_clickable(variable_name))
            self.logger.debug(f"{field_name} クリックできる状態")

        except TimeoutException as e:
            self.logger.error(f"{field_name} クリックが可能になるまで、{timeout}秒以上経過したためタイムアウト: {e}")
            raise

        except Exception as e:
            self.logger.error(f"{field_name} クリックが可能になるまでの待機中になんらかのエラーが発生: {e}")
            raise



# ----------------------------------------------------------------------------------
# # 指定の要素がDOM上に存在するまで待機

# self.driver_wait._dom_checker(by_pattern=, xpath=, field_name, timeout=timeout)

    def _dom_checker(self, by_pattern, xpath, field_name, timeout=10):
        try:
            WebDriverWait(self.chrome, timeout).until(EC.presence_of_element_located((self._locator_select(by_pattern), xpath)))
            self.logger.debug(f"{field_name} ページが更新されてます。")

        except TimeoutException as e:
            self.logger.error(f"{field_name} ページが更新されるまで、{timeout}秒以上経過したためタイムアウト: {e}")
            raise

        except Exception as e:
            self.logger.error(f"{field_name} ページが更新されるまでの待機中になんらかのエラーが発生: {e}")
            raise


# ----------------------------------------------------------------------------------


# #! サーバー用にスクショチェックができるように修正
# クリックができるようになるまで待機 デフォルト10秒
# self.driver_wait._element_clickable(by_pattern=, xpath=, timeout=)

    def _sever_element_clickable(self, by_pattern, element_path, notifyFunc, field_name, timeout=10):
        try:
            WebDriverWait(self.chrome, timeout).until(EC.element_to_be_clickable((self._locator_select(by_pattern), element_path)))
            self.logger.debug(f"{field_name} クリックできる状態")

        except TimeoutException as e:
            time_out_message = f"{field_name} クリックが可能になるまで、{timeout}秒以上経過したためタイムアウト: {e}"

            self.screenshot_process(message=time_out_message, notifyFunc=notifyFunc)

        except Exception as e:
            self.logger.error(f"{field_name} クリックが可能になるまでの待機中になんらかのエラーが発生: {e}")


# ----------------------------------------------------------------------------------
# スクショ撮影

    def _get_screenshot(self):
        # スクショ用のタイムスタンプ
        timestamp = datetime.now().strftime("%m-%d_%H-%M")

        filename = f"lister_page_{timestamp}.png"

        # 絶対path
        script_dir = os.path.dirname(os.path.abspath(__file__))

        # 現在のスクリプトの親ディレクトリのパス
        parent_dir = os.path.dirname(script_dir)

        # スクショ保管場所の絶対path
        screenshot_dir = os.path.join(parent_dir, 'DebugScreenshot/')

        # もしディレクトリがなかったら作成
        if not os.path.exists(screenshot_dir):
            os.makedirs(screenshot_dir)
            self.logger.debug(f"ディレクトリがなかったため作成{screenshot_dir}")

        full_path = os.path.join(screenshot_dir, filename)

        # スクリーンショットを保存
        screenshot_saved = self.chrome.save_screenshot(full_path)
        if screenshot_saved:
            self.logger.debug(f"スクリーンショットを保存: {full_path}")

        return full_path


# ----------------------------------------------------------------------------------
# スクショ削除

    def _delete_screenshot(self, screenshot_path):
        try:
            self.logger.info(f"********** _delete_screenshot start **********")

            self.logger.debug(f"screenshot_path: {screenshot_path}")

            if screenshot_path and os.path.exists(screenshot_path):
                os.remove(screenshot_path)
                self.logger.debug(f"スクショの削除、完了: {screenshot_path}")

            else:
                self.logger.error(f"スクショが見つかりません: {screenshot_path}")


            self.logger.info(f"********** _delete_screenshot end **********")

        except Exception as e:
            self.logger.error(f"_delete_screenshot 処理中にエラーが発生:{e}")
            raise


# ----------------------------------------------------------------------------------
# スクショプロセス

    def screenshot_process(self, message, notifyFunc):
        try:
            self.logger.info(f"********** screenshot_process start **********")

            # スクショを撮影
            screenshot_path = self._get_screenshot()

            # スクショを添付して通知
            notifyFunc(message, screenshot_path)

            # スクショを削除
            self._delete_screenshot(screenshot_path)

            self.logger.info(f"********** screenshot_process end **********")


        except Exception as e:
            self.logger.error(f"screenshot_process 処理中にエラーが発生:{e}")
            raise


# ----------------------------------------------------------------------------------
# titleが合致してたら待機を解除
# JavaScriptでのちゃんとサイトが開いてるのか確認

    def js_and_title_check(self, url ,gss_title, field_name, token, notifyFunc=None):
        try:
            self.logger.info(f"********** {field_name} js_and_title_check start **********")

            self.logger.debug(f"url: {url}")
            self.logger.debug(f"input_title: {gss_title}")

            response = requests.get(url)
            response.raise_for_status()

            soup = BeautifulSoup(response.text, 'html.parser')
            title = soup.title.string

            time.sleep(2)

            # 開いてるサイトのtitleを取得
            site_title = title

            if site_title==gss_title:
                self.logger.info(f"title、一致してます。\ngss_title:{gss_title[:10]}")

            else:
                title_error_msg = (f"title、スプシに入力されてるtitleと一致しません。\ngss_title:\n{gss_title}\n\nsite_title:\n{site_title}")
                self.logger.error(title_error_msg)

                # 通知が必要な場合にいれる
                if notifyFunc:
                    notifyFunc(token, title_error_msg)

            self.logger.info(f"********** {field_name} js_and_title_check end **********")


        except Exception as e:
            self.logger.error(f"js_and_title_check 処理中にエラーが発生:{e}")
            raise


# ----------------------------------------------------------------------------------
# **********************************************************************************
