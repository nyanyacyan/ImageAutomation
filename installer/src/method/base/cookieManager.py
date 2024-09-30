# coding: utf-8
# $$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$

# $$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$
# import
import time, sqlite3
from typing import Any
from selenium.webdriver.chrome.webdriver import WebDriver


# 自作モジュール
from .utils import Logger
from .SQLite import SQLite
from ..const import Filename
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
        self.currentTime = int(time.time())

        # インスタンス
        self.sqlite = SQLite(fileName=self.fileName, debugMode=debugMode)


# ----------------------------------------------------------------------------------
# Flow

    @decoInstance.funcBase
    def checkCookieInDB(self):
        cookieAllData = self.startDBCheck()
        if cookieAllData:
            if len(cookieAllData) > 1:
                return self.deleteAllCookies()
            else:
                self.logger.info("DBにCookieデータの存在を確認。既存のCookieを使ってログイン")
                return self.checkCookieLimit()
        else:
            self.logger.warning("テーブルは存在するが、値が入っていません")
            self.sqlite.resetTable()
            return self.insertData()


# ----------------------------------------------------------------------------------


    @decoInstance.funcBase
    def insertData(self):
        self.insertSqlite()
        return self.checkCookieLimit()


# ----------------------------------------------------------------------------------


    @decoInstance.funcBase
    def deleteAllCookies(self):
        self.logger.warning(f"既存データが1つ以上あるため全てクリアします")
        self.sqlite.resetTable()
        self.insertSqlite()
        return self.checkCookieLimit()


# ----------------------------------------------------------------------------------
# # SQLiteにCookieのデータから有効期限を確認する

    @decoInstance.funcBase
    def checkCookieLimit(self, col: str='id', value: Any=1):
        cookieAllData = self.getCookieInSqlite(col=col, value=value)
        self.logger.warning(f"cookieAllData: {cookieAllData}")

        if cookieAllData:
            nameValue = cookieAllData[1]
            expiresValue = cookieAllData[5]   # タプルの場合には数値で拾う
            maxAgeValue = cookieAllData[6]
            createTimeValue = cookieAllData[7]

            self.logger.warning(f"nameValue: {nameValue}")
            self.logger.warning(f"expiresValue: {expiresValue}")
            self.logger.warning(f"maxAgeValue: {maxAgeValue}")


            if maxAgeValue:
                return self.getMaxAgeLimit(maxAgeValue=maxAgeValue, createTimeValue=createTimeValue)

            elif expiresValue:
                return self.getExpiresLimit(expiresValue=expiresValue)

            elif nameValue:
                self.logger.warning(f"有効期限のないCookieを取得。CookieのSave開始")
                return self.createCookieFile()

            else:
                self.logger.warning("Cookieの有効期限が設定されてません")
                return None

        else:
            self.logger.error(f"cookieが存在しません: {cookieAllData}")
            return None


# ----------------------------------------------------------------------------------


    @property
    def getCookies(self):
        return self.chrome.get_cookies()


# ----------------------------------------------------------------------------------


    @property
    def getCookie(self):
        cookies = self.getCookies
        return cookies[0]


# ----------------------------------------------------------------------------------
# 指定するSQLiteからcookieのデータを取得

    def getCookieInSqlite(self, col: str='id', value: Any=1):
        return self.sqlite.getRowRecordsByCol(col=col, value=value)


# ----------------------------------------------------------------------------------
# 指定するSQLiteからcookieのデータを取得

    def startDBCheck(self):
        return self.sqlite.startGetAllRecordsByCol()


# ----------------------------------------------------------------------------------
# SQLiteにcookiesの情報を書き込めるようにするための初期設定

    def createCookieDB(self):
        return self.sqlite.createCookieDB()


# ----------------------------------------------------------------------------------
# SQLiteにCookieのデータを書き込む
# expiresよりもMaxAgeが優先される、〇〇秒間、持たせる権限

    @decoInstance.funcBase
    def insertSqlite(self):
        cookie = self.getCookie
        self.logger.debug(f"cookie: {cookie}")
        cookieName = cookie['name']
        cookieValue = cookie.get('value')
        cookieDomain = cookie.get('domain')
        cookiePath = cookie.get('path')
        cookieExpires = cookie.get('expires') if 'expires' in cookie else None
        cookieMaxAge = cookie.get('max-age') if 'max-age' in cookie else None
        cookieCreateTime = int(time.time())

        col = ('name', 'value', 'domain', 'path', 'expires', 'maxAge', 'createTime')
        values = (cookieName, cookieValue, cookieDomain, cookiePath, cookieExpires, cookieMaxAge, cookieCreateTime)
        self.logger.warning(f"values: {values}")

        self.sqlite.insertData(col=col, values=values)


# ----------------------------------------------------------------------------------
# max-ageの時間の有効性を確認する

    @decoInstance.funcBase
    def getMaxAgeLimit(self, maxAgeValue: int, createTimeValue: int):
        limitTime = maxAgeValue + createTimeValue

        if self.currentTime < limitTime:
            self.logger.info("[MaxAge]cookieが有効: Cookieを使ってログイン")
            return self.createCookieFile()
        else:
            self.logger.error("有効期限切れのcookie: 既存のCookieを消去して再度IDログイン実施")
            self.deleteRecordsProcess()
            return None


# ----------------------------------------------------------------------------------
# expiresの時間の有効性を確認する

    @decoInstance.funcBase
    def getExpiresLimit(self, expiresValue: int):
        if self.currentTime < expiresValue:
            self.logger.info("[expires]cookieが有効: Cookieを使ってログイン")
            return self.createCookieFile()

        else:
            self.logger.error("有効期限切れのcookie: 既存のCookieを消去して再度IDログイン実施")
            self.deleteRecordsProcess()
            return None


# ----------------------------------------------------------------------------------
# 削除が完了したあとにIDを取得する

    def deleteRecordsProcess(self, col: str='id', value: Any=1):
        self.sqlite.deleteRecordsByCol(col=col, value=value)
        self.insertSqlite()
        return self.createCookieFile()


# ----------------------------------------------------------------------------------
# SQLiteからcookieを復元

    @decoInstance.funcBase
    def createCookieFile(self):
        cookieAllData = self.getCookieInSqlite()

        if cookieAllData:
            cookie = {
                'name': cookieAllData[1],
                'value': cookieAllData[2],
                'domain': cookieAllData[3],
                'path': cookieAllData[4],
            }

            if cookieAllData[6]:
                cookie['expires'] = self.currentTime + cookieAllData[6]
            elif cookieAllData[5]:
                cookie['expires'] = cookieAllData[5]
            self.logger.warning(f"cookie:\n{cookie}")

            return cookie


# ----------------------------------------------------------------------------------

