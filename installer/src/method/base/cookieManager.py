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
from ..const import Filename
from .loginWithId import IdLogin


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
        self.idLogin = IdLogin(debugMode=debugMode)

# ----------------------------------------------------------------------------------
# Flow > 真偽値を返す > True=cookieLogin > False=IDLogin
# SQLiteにCookieのデータから有効期限を確認する

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

# SQLiteにcookiesの情報を書き込めるようにするための初期設定

    def createCookieDB(self):
        sql = f'''
            CREATE TABLE IF NOT EXISTS {self.fileName} (
                id INTEGER PRIMARY KEY AUTOINCREMENT,   # 一意の認識キーに設定、１〜順番に連番発行される
                name TEXT NOT NULL,
                value TEXT NOT NULL,
                domain TEXT,
                path TEXT,
                expires INTEGER,
                maxAge INTEGER,
                createTime INTEGER
            )
        '''

        self.sqlite.createTable(sql=sql)


# ----------------------------------------------------------------------------------
# SQLiteにCookieのデータを書き込む

    def insertSqlite(self):
        cookie = self.getCookie
        cookieName = cookie['name']
        cookieValue = cookie.get('value')
        cookieDomain = cookie.get('domain')
        cookiePath = cookie.get('path')
        cookieExpires = cookie.get('expires')
        cookieMaxAge = cookie.get('max-age')  # expiresよりも優先される、〇〇秒間、持たせる権限
        cookieCreateTime = int(time.time())

        col = ('name', 'value', 'domain', 'path', 'expires', 'maxAge', 'createTime')
        values = (cookieName, cookieValue, cookieDomain, cookiePath, cookieExpires, cookieMaxAge, cookieCreateTime)

        self.sqlite.insertTable(col=col, values=values)


# ----------------------------------------------------------------------------------
# max-ageの時間の有効性を確認する

    def getMaxAgeLimit(self, maxAgeValue: int, createTimeValue: int):
        limitTime = maxAgeValue + createTimeValue

        if self.currentTime < limitTime:
            self.logger.info("cookieが有効: 既存のCookieを使ってログイン")
            return self.createCookieFile()
        else:
            self.logger.error("有効期限切れのcookie: 既存のCookieを消去して再度IDログイン実施")
            self.deleteRecordsProcess()
            return None


# ----------------------------------------------------------------------------------
# expiresの時間の有効性を確認する

    def getExpiresLimit(self, expiresValue: int):
        if self.currentTime > expiresValue:
            self.logger.info("cookieが有効: 既存のCookieを使ってログイン")
            return self.createCookieFile()

        else:
            self.logger.error("有効期限切れのcookie: 既存のCookieを消去して再度IDログイン実施")
            self.deleteRecordsProcess()
            return None


# ----------------------------------------------------------------------------------
# 削除が完了したあとにIDを取得する

    def deleteRecordsProcess(self, col: str='id', value: Any=1):
        return self.sqlite.deleteRecordsByCol(col=col, value=value)


# ----------------------------------------------------------------------------------
# SQLiteからcookieを復元

    def createCookieFile(self):
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

            return cookie


# ----------------------------------------------------------------------------------
