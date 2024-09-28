# coding: utf-8
# $$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$

# $$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$
# import
from selenium.webdriver.chrome.webdriver import WebDriver


# 自作モジュール
from .utils import Logger
from .SQLite import SQLite
from ..const import Filename


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

        # インスタンス
        self.sqlite = SQLite(fileName=self.fileName, debugMode=debugMode)

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
# SQLiteにCookieのデータを書き込む

    def insertSqlite(self):
        cookie = self.getCookie
        cookieName = cookie['name']
        cookieValue = cookie.get('value')
        cookieDomain = cookie.get('domain')
        cookiePath = cookie.get('path')
        cookieExpires = cookie.get('expires')
        cookieMaxAge = cookie.get('max-age')  # expiresよりも優先される

        col = ('name', 'value', 'domain', 'path', 'expires', 'max_age')
        values = (cookieName, cookieValue, cookieDomain, cookiePath, cookieExpires, cookieMaxAge)

        self.sqlite.insertTable(col=col, values=values)


# ----------------------------------------------------------------------------------
# SQLiteにcookiesの情報を書き込めるようにするための初期設定

    def createCookieDB(self):
        sql = f'''
            CREATE TABLE IF NOT EXISTS {self.fileName} (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                value TEXT NOT NULL,
                domain TEXT,
                path TEXT,
                expires INTEGER,
                max_age INTEGER
            )
        '''

        self.sqlite.createTable(sql=sql)


# ----------------------------------------------------------------------------------
# SQLiteにCookieのデータを入れ込む