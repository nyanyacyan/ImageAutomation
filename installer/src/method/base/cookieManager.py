# coding: utf-8
# $$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$

# $$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$
# import
import time
from typing import Any
from selenium.webdriver.chrome.webdriver import WebDriver


# 自作モジュール
from .utils import Logger
from .SQLite import SQLite
from ..const import Filename, ColumnsName
from .decorators import Decorators

decoInstance = Decorators(debugMode=True)


# $$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$
# **********************************************************************************


class CookieManager:
    def __init__(self, chrome: WebDriver, homeUrl: str, debugMode=True):
        # logger
        self.getLogger = Logger(__name__, debugMode=debugMode)
        self.logger = self.getLogger.getLogger()

        self.chrome = chrome
        self.homeUrl = homeUrl
        self.fileName = Filename.Cookie.value
        self.columnsName = ColumnsName.Cookies.value
        self.currentTime = int(time.time())

        # インスタンス
        self.sqlite = SQLite(fileName=self.fileName, debugMode=debugMode)

# ----------------------------------------------------------------------------------
# start①
# DBが存在確認

    @decoInstance.funcBase
    def startDBExists(self):
        DBBool = self.sqlite.tableExists()
        if DBBool:
            return self.cookieDataExistsInDB()
        else:
            self.logger.warning(f"{Filename} が作られてません。これよりテーブル作成開始")
            return self.sqlite.createTable()

# ----------------------------------------------------------------------------------
# ②
# DBにCookieの存在確認

    @decoInstance.funcBase
    def cookieDataExistsInDB(self):
        DBColNames = self.sqlite.columnsExists()
        result = all(cokName in self.columnsName for cokName in DBColNames)
        if result is True:
            self.checkCookieLimit()
        else:
            self.logger.warning(f"{Filename} のテーブルデータがありません。Cookieを取得します")



# ----------------------------------------------------------------------------------
# ③
# DBにあるCookieの有効期限が有効化を確認

    @decoInstance.funcBase
    def checkCookieLimit(self, col: str='id', value: Any=1):
        cookieAllData = self.getCookieInSqlite(col=col, value=value)

        if cookieAllData:
            expiresValue = cookieAllData[5]   # タプルの場合には数値で拾う
            maxAgeValue = cookieAllData[6]
            createTimeValue = cookieAllData[7]

            if maxAgeValue:
                return self.getMaxAgeLimit(maxAgeValue=maxAgeValue, createTimeValue=createTimeValue)

            elif expiresValue:
                return self.getExpiresLimit(expiresValue=expiresValue)

            else:
                self.logger.warning("Cookieの有効期限が設定されてません")
                return None

        else:
            self.logger.error(f"cookieが存在しません: {cookieAllData}")
            return None


# ----------------------------------------------------------------------------------
# ④
# Cookieがちゃんと取得できてるかどうかを確認
# リトライ実施


    @decoInstance.noneRetryAction()
    def getCookie(self):
        cookies = self.getCookies()
        self.logger.warning(f"cookies: {cookies}")
        cookie = cookies[0]
        return cookie


# ----------------------------------------------------------------------------------
# ⑤
# Cookieの値が入っているか確認

    def canValueInCookie(self, cookie: dict):
        if not cookie.get('name') or not cookie.get('value'):
            self.logger.warning(f"cookieに必要な情報が記載されてません")
            return None


# ----------------------------------------------------------------------------------
# 有効期限をクリアしたmethod
# DBよりcookie情報を取得する

    @decoInstance.funcBase
    def insertCookieData(self, cookie):

        cookieName = cookie['name']
        cookieValue = cookie.get('value')
        cookieDomain = cookie.get('domain')
        cookiePath = cookie.get('path')
        cookieExpires = cookie.get('expires')
        cookieMaxAge = cookie.get('max-age')  # expiresよりも優先される、〇〇秒間、持たせる権限
        cookieCreateTime = int(time.time())

        values = (cookieName, cookieValue, cookieDomain, cookiePath, cookieExpires, cookieMaxAge, cookieCreateTime)

        self.sqlite.insertData(col=self.columnsName, values=values)


# ----------------------------------------------------------------------------------
# SQLiteからcookieを復元

    @decoInstance.funcBase
    def cookieMakeAgain(self):
        cookieAllData = self.getCookieInSqlite()

        if cookieAllData:
            cookie = {
                'name': cookieAllData[0],
                'value': cookieAllData[1],
                'domain': cookieAllData[2],
                'path': cookieAllData[3],
            }

            if cookieAllData[5]:
                cookie['expiry'] = self.currentTime + cookieAllData[5]
            elif cookieAllData[4]:
                cookie['expiry'] = cookieAllData[4]
            self.logger.warning(f"cookie:\n{cookie}")

            return cookie


# ----------------------------------------------------------------------------------

# ----------------------------------------------------------------------------------
# Cookieの取得成功method

    @decoInstance.funcBase
    def processValidCookie(self):
        self.sqlite.createTable()
        self.insertCookieData()
        return self.checkCookieLimit()


# ----------------------------------------------------------------------------------

# 指定するSQLiteからcookieのデータを取得

    def getCookieInSqlite(self, col: str='id', value: Any=1):
        return self.sqlite.getRowRecordsByCol(col=col, value=value)


# ----------------------------------------------------------------------------------
# SQLiteにCookieのデータから有効期限を確認する

    @decoInstance.funcBase
    def checkCookieLimit(self, col: str='id', value: Any=1):
        cookieAllData = self.getCookieInSqlite(col=col, value=value)

        if cookieAllData:
            expiresValue = cookieAllData[5]   # タプルの場合には数値で拾う
            maxAgeValue = cookieAllData[6]
            createTimeValue = cookieAllData[7]

            if maxAgeValue:
                return self.getMaxAgeLimit(maxAgeValue=maxAgeValue, createTimeValue=createTimeValue)

            elif expiresValue:
                return self.getExpiresLimit(expiresValue=expiresValue)

            else:
                self.logger.warning("Cookieの有効期限が設定されてません")
                return None

        else:
            self.logger.error(f"cookieが存在しません: {cookieAllData}")
            return None


# ----------------------------------------------------------------------------------



    def getCookies(self):
        return self.chrome.get_cookies()


# ----------------------------------------------------------------------------------


    @decoInstance.noneRetryAction()
    def getfirstCookie(self):
        cookies = self.getCookies()
        self.logger.warning(f"cookies: {cookies}")
        cookie = cookies[0]

        if not cookie.get('name') or not cookie.get('value'):
            self.logger.warning(f"cookieに必要な情報が記載されてません")
            return None


# ----------------------------------------------------------------------------------

# max-ageの時間の有効性を確認する

    @decoInstance.funcBase
    def getMaxAgeLimit(self, maxAgeValue: int, createTimeValue: int):
        limitTime = maxAgeValue + createTimeValue

        if self.currentTime < limitTime:
            self.logger.info("cookieが有効: 既存のCookieを使ってログイン")
            return self.cookieMakeAgain()
        else:
            self.logger.error("有効期限切れのcookie: 既存のCookieを消去して再度IDログイン実施")
            self.deleteRecordsProcess()
            return None


# ----------------------------------------------------------------------------------
# expiresの時間の有効性を確認する

    @decoInstance.funcBase
    def getExpiresLimit(self, expiresValue: int):
        if self.currentTime < expiresValue:
            self.logger.info("cookieが有効: 既存のCookieを使ってログイン")
            return self.cookieMakeAgain()

        else:
            self.logger.error("有効期限切れのcookie: 既存のCookieを消去して再度IDログイン実施")
            self.deleteRecordsProcess()
            return None


# ----------------------------------------------------------------------------------
# 削除が完了したあとにIDを取得する

    def deleteRecordsProcess(self, col: str='id', value: Any=1):
        return self.sqlite.deleteRecordsByCol(col=col, value=value)


# ----------------------------------------------------------------------------------


