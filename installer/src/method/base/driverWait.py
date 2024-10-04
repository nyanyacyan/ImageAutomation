# coding: utf-8
# $$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$

# $$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$
# import

from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

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
# クリックができるまで待機

    def canWaitClick(self, by: str, value: str, timeout: int = 10):
        return WebDriverWait(self.chrome, timeout).until(EC.element_to_be_clickable(by, value))


# ----------------------------------------------------------------------------------
# ページが完全に開くまで待機

    def loadPageWait(self, by: str, value: str, timeout: int = 10):
        return WebDriverWait(self.chrome, timeout).until(EC.visibility_of_element_located((by, value)))


# ----------------------------------------------------------------------------------
# DOM上に存在するまで待機

    def canWaitDom(self, by: str, value: str, timeout: int = 10):
        return WebDriverWait(self.chrome, timeout).until(EC.presence_of_element_located((self._locator_select(by), value)))


# ----------------------------------------------------------------------------------
# 指定のURLに切り替わるまで待機

    def changeUrlWait(self, by: str, Url: str, timeout: int = 10):
        return WebDriverWait(self.chrome, timeout).until(EC.url_changes(Url))


# ----------------------------------------------------------------------------------
# **********************************************************************************
