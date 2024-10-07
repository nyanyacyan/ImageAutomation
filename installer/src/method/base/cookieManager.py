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
from ..const import TableName, ColumnsName
from ..constSqliteTable import TableSchemas
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
        self.tableName = TableName.Cookie.value

        self.columnsName = ColumnsName.Cookies.value
        self.primaryKey = ColumnsName.PRIMARY_KEY.value
        self.currentTime = int(time.time())

        # インスタンス
        self.sqlite = SQLite(tableName=self.tableName, debugMode=debugMode)


# ----------------------------------------------------------------------------------
# start①
# DBが存在確認

    @decoInstance.funcBase
    def startBoolFilePath(self):
        tableBool = self.sqlite.boolFilePath()
        sqlCookieAllData = self.sqlite.getRecordsAllData(tableName=self.tableName)
        cookieDataCount = len(sqlCookieAllData)
        self.logger.warning(f"cookieDataCount: {cookieDataCount}")
        if 5 < cookieDataCount:
            self.sqlite.getSqlOldData(tableName=self.tableName, primaryKey=self.primaryKey)

        if tableBool:
            return self.cookieDataExistsInDB()
        else:
            self.logger.debug(f"{self.tableName} が作られてません。これよりテーブル作成開始")
            self.sqlite.isFileExists()  # ファイルを作成
            self.sqlite.createAllTable()  # 全てのテーブルを作成
            return self.getCookieFromAction()


# ----------------------------------------------------------------------------------
# ②
# DBにCookieの存在確認

    @decoInstance.funcBase
    def cookieDataExistsInDB(self):
        DBColNames = self.sqlite.columnsExists(tableName=self.tableName)

        self.logger.debug(f"DBColNames: {DBColNames}")
        self.logger.debug(f"self.columnsName: {self.columnsName}")

        # self.columnsNameの中にあるものがDBColNamesに全て入っているのかを確認
        result = all(cokName in DBColNames for cokName in self.columnsName)
        if result is True:
            self.logger.info(f"cookieデータを確認できました\n{DBColNames}")
            return self.checkCookieLimit()
        else:
            self.logger.warning(f"{self.tableName} のテーブルデータがありません。Cookieを取得します")
            return self.getCookieFromAction()


# ----------------------------------------------------------------------------------
# ③
# DBにあるCookieの有効期限が有効化を確認

    @decoInstance.funcBase
    def checkCookieLimit(self):
        newCookieData = self.sqlite.getColMaxValueRow(tableName=self.tableName, primaryKey=self.primaryKey)

        if newCookieData:
            expiresValue = newCookieData[5]   # タプルの場合には数値で拾う
            maxAgeValue = newCookieData[6]
            createTimeValue = newCookieData[7]

            if maxAgeValue:
                return self.getMaxAgeLimit(maxAgeValue=maxAgeValue, createTimeValue=createTimeValue)

            elif expiresValue:
                return self.getExpiresLimit(expiresValue=expiresValue)

            else:
                self.logger.warning("Cookieの有効期限が設定されてません")
                return self.getCookieFromAction()

        else:
            self.logger.error(f"cookieが存在しません: {newCookieData}")
            return self.getCookieFromAction()


# ----------------------------------------------------------------------------------


    @decoInstance.noneRetryAction()
    def getCookieFromAction(self):
        cookie = self.getCookie()
        Cookie = self.insertCookieData(cookie=cookie)
        return self.canValueInCookie(cookie=Cookie)


# ----------------------------------------------------------------------------------
# ④
# Cookieがちゃんと取得できてるかどうかを確認
# リトライ実施

    @decoInstance.funcBase
    def getCookie(self):
        cookies = self.getCookies()
        self.logger.debug(f"cookies: {cookies}")
        cookie = cookies[0]
        if cookie:
            return cookie
        else:
            return None


# ----------------------------------------------------------------------------------


    def getCookies(self):
        return self.chrome.get_cookies()


# ----------------------------------------------------------------------------------
# # ⑤
# Cookieの値が入っているか確認

    @decoInstance.funcBase
    def canValueInCookie(self, cookie: dict):
        if not cookie.get('name') or not cookie.get('value'):
            self.logger.warning(f"cookieに必要な情報が記載されてません")
            return None
        else:
            return cookie


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

        # 値をtuple化
        values = (cookieName, cookieValue, cookieDomain, cookiePath, cookieExpires, cookieMaxAge, cookieCreateTime)

        # データを入れ込む
        self.sqlite.insertData(tableName=self.tableName, col=self.columnsName, values=values)
        return cookie


# ----------------------------------------------------------------------------------
# SQLiteからcookieを復元

    @decoInstance.funcBase
    def cookieMakeAgain(self):
        cookieAllData = self.sqlite.getColMaxValueRow(tableName=self.tableName, primaryKey=self.primaryKey)
        cookieData = cookieAllData[0]

        if cookieAllData:
            cookie = {
                'name': cookieData[1],
                'value': cookieData[2],
                'domain': cookieData[3],
                'path': cookieData[4],
            }

            if cookieData[6]:
                cookie['expires'] = self.currentTime + cookieData[6]
            elif cookieData[5]:
                cookie['expires'] = cookieData[5]
            self.logger.debug(f"cookie:\n{cookie}")

            return cookie


# ----------------------------------------------------------------------------------
# SQLiteにCookieのデータから有効期限を確認する

    @decoInstance.funcBase
    def checkCookieLimit(self):
        cookieAllData = self.sqlite.getColMaxValueRow(tableName=self.tableName, primaryKey=self.primaryKey)

        if cookieAllData:
            cookieData = cookieAllData[0]
            expiresValue = cookieData[5]   # タプルの場合には数値で拾う
            maxAgeValue = cookieData[6]
            createTimeValue = cookieData[7]

            if maxAgeValue:
                return self.getMaxAgeLimit(maxAgeValue=maxAgeValue, createTimeValue=createTimeValue)

            elif expiresValue:
                return self.getExpiresLimit(expiresValue=expiresValue)

            else:
                self.logger.warning("Cookieの有効期限が設定されてません")
                return None

        else:
            self.logger.error(f"cookieが存在しません: {cookieData}")
            return None


# ----------------------------------------------------------------------------------
# max-ageの時間の有効性を確認する

    @decoInstance.funcBase
    def getMaxAgeLimit(self, maxAgeValue: int, createTimeValue: int):
        limitTime = maxAgeValue + createTimeValue

        if self.currentTime < limitTime:
            self.logger.info("cookieが有効: 既存のCookieを使ってログインを行います")
            return self.cookieMakeAgain()
        else:
            self.logger.error("有効期限切れのcookie: 既存のCookieを消去して再度IDログイン実施")
            return self.getCookieFromAction()



# ----------------------------------------------------------------------------------
# expiresの時間の有効性を確認する

    @decoInstance.funcBase
    def getExpiresLimit(self, expiresValue: int):
        if self.currentTime < expiresValue:
            self.logger.info("cookieが有効: 既存のCookieを使ってログインを行います")
            return self.cookieMakeAgain()
        else:
            self.logger.error("有効期限切れのcookie: 既存のCookieを消去して再度IDログイン実施")
            return self.getCookieFromAction()


# ----------------------------------------------------------------------------------

