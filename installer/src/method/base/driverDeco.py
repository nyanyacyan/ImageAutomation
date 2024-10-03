# coding: utf-8
# $$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$

# $$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$
# import
import time
from functools import wraps
from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait


# 自作モジュール
from .utils import Logger


# $$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$
# **********************************************************************************

class jsCompleteWaitDeco:
    def __init__(self, debugMode=True):

        # logger
        self.getLogger = Logger(__name__, debugMode=debugMode)
        self.logger = self.getLogger.getLogger()


# ----------------------------------------------------------------------------------
# func > jsCompleteWait > refresh > retry

    def jsCompleteWait(self, maxRetry: int=2, delay: int=2, timeout: int = 10):
        def decorator(func):
            @wraps(func)
            def wrapper(instance, *args, **kwargs):
                self.logger.info(f"引数:\nargs={args}, kwargs={kwargs}")
                retryCount = 0
                while retryCount < maxRetry:
                    try:
                        self.logger.info(f"********** {func.__name__} start {retryCount + 1}回目 **********")

                        chrome = instance.chrome

                        result = func(instance, *args, **kwargs)

                        self.jsPageChecker(chrome=chrome, timeout=timeout)

                        return result

                    except TimeoutException as e:
                        retryCount += 1
                        if retryCount < maxRetry:
                            self.logger.error(f"{func.__name__}: {timeout}秒以上経過したためタイムアウト\nページを更新してリトライ実施: {retryCount} 回目")
                            time.sleep(delay)
                            chrome.refresh()
                            continue

                        else:
                            self.logger.error(f"{func.__name__}: リトライ上限まで実施")

                    except Exception as e:
                        self.logger.error(f"{func.__name__} ページが更新されるまでの待機中になんらかのエラーが発生: {e}")
                        break
            return wrapper
        return decorator


# ----------------------------------------------------------------------------------
# 次のページに移動後にページがちゃんと開いてる状態か全体を確認してチェックする

    def jsPageChecker(self, chrome: WebDriver, timeout: int = 10):
            if WebDriverWait(chrome, timeout).until(lambda driver: driver.execute_script('return document.readyState')=='complete'):
                self.logger.debug(f"{__name__} ページが更新OK")


# ----------------------------------------------------------------------------------
