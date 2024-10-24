# coding: utf-8
# $$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$
# 2024/9/23 更新

# sudo tree /Users/nyanyacyan/Desktop/Project_file/SNS_auto_upper -I 'venv|pyvenv.cfg|__pycache__'


# $$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$
# import
import os
from dotenv import load_dotenv

# 自作モジュール
from base.utils import Logger
from base.chrome import ChromeManager
from base.cookieManager import CookieManager
from base.loginWithCookie import CookieLogin
from base.dataInSqlite import DataInSQLite
from const import SiteUrl
from constElementPath import LoginElement

load_dotenv()

# $$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$
# **********************************************************************************
# 一連の流れ

class Flow:
    def __init__(self, debugMode=True):

        # logger
        self.getLogger = Logger(__name__, debugMode=debugMode)
        self.logger = self.getLogger.getLogger()

        self.chrome = ChromeManager(debugMode=debugMode)
        self.loginUrl = SiteUrl.LoginUrl.value
        self.homeUrl = SiteUrl.HomeUrl.value
        self.targetUrl = SiteUrl.TargetUrl.value

        # インスタンス
        self.cookieManager = CookieManager(chrome=self.chrome, homeUrl=self.homeUrl, debugMode=debugMode)
        self.cookieLogin = CookieLogin(chrome=self.chrome, loginUrl=self.loginUrl, homeUrl=self.logger, debugMode=debugMode)
        self.dataInSQLite = DataInSQLite(chrome=self.chrome, debugMode=debugMode)


# ----------------------------------------------------------------------------------

# TODO ログイン
    def flow(self):
        # DBチェッカーから
        cookies = self.cookieManager.startBoolFilePath()

        # ログイン情報を呼び出し
        loginInfo = LoginElement.LOGIN_INFO.value
        loginInfo['idText'] = os.getenv("ID")
        loginInfo['passText'] = os.getenv("PASS")

        # cookiesの出力によってログイン方法を分ける
        self.cookieLogin.flowSwitchLogin(cookies=cookies, loginInfo=loginInfo)

        # text, imageを取得してSQLiteに入れ込む→入れ込んだIDのリストを返す
        allIDList = self.dataInSQLite.flowCollectElementDataToSQLite(targetUrl=self.targetUrl)

        return allIDList

# TODO batFileの作成→実行、install

# TODO 手順書の作成




# ----------------------------------------------------------------------------------


if __name__ == "__main__":
    process = Flow(debugMode=True)

    process.flow()