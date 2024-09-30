# coding: utf-8
# $$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$
# テストOK
# $$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$
# import
import sqlite3
from typing import Any


# 自作モジュール
from .utils import Logger
from .path import BaseToPath
from .errorHandlers import NetworkHandler


# $$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$
# **********************************************************************************
# 一連の流れ

class SQLite:
    def __init__(self, fileName: str, debugMode=True):

        # logger
        self.getLogger = Logger(__name__, debugMode=debugMode)
        self.logger = self.getLogger.getLogger()

        self.fileName = fileName

        # インスタンス化
        self.networkError = NetworkHandler(debugMode=debugMode)
        self.path = BaseToPath(debugMode=debugMode)


# ----------------------------------------------------------------------------------


    def getDBFullPath(self):
        dbFilePath = self.path.getResultSubDirDBFilePath()
        if not dbFilePath.exists():
            try:
                conn = sqlite3.connect(dbFilePath)
                conn.close()
                return dbFilePath

            except sqlite3.OperationalError as e:
                self.logger.error(f"dbFullPath: {dbFilePath}")
                self.logger.error(f"データベース接続エラー: {e}")
                raise

        return dbFilePath


# ----------------------------------------------------------------------------------
# params: tuple = ()　> パラメータが何もなかったら空にするという意味


    def SQLPromptBase(self, sql: str, params: tuple = (), fetch: str = None):
        conn = self.getDBconnect()
        try:
            c = conn.cursor()  # DBとの接続オブジェクトを受け取って通信ができるようにする
            c.execute(sql, params)  # 実行するSQL文にて定義して実行まで行う

            if fetch == 'one':
                return c.fetchone()
            elif fetch == 'all':
                return c.fetchall()
            else:
                return None

        except sqlite3.OperationalError as e:
            if 'no such table' in str(e):
                self.logger.warning(f"テーブルが存在しません: {e}")
                self.createTable()

        except Exception as e:
            conn.rollback()
            self.logger.error(f"エラーが発生しました。トランザクションをロールバックしました:{e}")  # ロールバックは変更する前の状態に戻すこと

        finally:
            conn.close()

# ----------------------------------------------------------------------------------


    def getDBconnect(self) -> sqlite3.Connection:
        dbFullPath = self.getDBFullPath()
        try:
            conn = sqlite3.connect(dbFullPath)
            return conn
        except sqlite3.OperationalError as e:
            self.logger.error(f"dbFullPath: {dbFullPath}")
            self.logger.error(f"データベース接続エラー: {e}")
            raise



# ----------------------------------------------------------------------------------

# SQLiteにcookiesの情報を書き込めるようにするための初期設定

    def createTable(self):
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
        self.SQLPromptBase(sql=sql, fetch=None)
        return self.logger.info(f"{self.fileName} テーブルを作成")


# ----------------------------------------------------------------------------------
# SQLiteへ入れ込む

    def insertTable(self, col: tuple, values: tuple):
        placeholders = ', '.join(['?' for _ in values]) # valuesの数の文？を追加して結合
        sql = f"INSERT INTO {self.fileName} {col} VALUES {placeholders}"
        self.SQLPromptBase(sql=sql, fetch=None)
        return self.logger.info(f"【success】{self.fileName} テーブルにデータを追加")

# ----------------------------------------------------------------------------------
# テーブルデータを全て引っ張る

    def getRecordsAllData(self):
            sql = f"SELECT * FROM {self.fileName}"
            self.SQLPromptBase(sql=sql, fetch='all')
            return self.logger.info(f"【success】{self.fileName} すべてのデータを抽出")


# ----------------------------------------------------------------------------------
# 指定したColumnの値を指定して行を抽出 > Column=name Value=5 > 指定の行を抜き出す > List

    def getAllRecordsByCol(self, col: str, value: Any):
        sql = f"SELECT * FROM {self.fileName} WHERE {col} = ?"
        self.SQLPromptBase(sql=sql, params=(value, ), fetch='all')
        return self.logger.info(f"【success】{self.fileName} 指定のカラムデータをすべて抽出")



# ----------------------------------------------------------------------------------
# 指定したColumnの値を指定して行を抽出 > Column=name Value=5 > 指定の行を抜き出す > row

    def getRowRecordsByCol(self, col: str, value: Any):
        sql = f"SELECT * FROM {self.fileName} WHERE {col} = ?"
        self.SQLPromptBase(sql=sql, params=(value, ), fetch=None)
        return self.logger.info(f"【success】{self.fileName} 指定の行のデータを抽出")



# ----------------------------------------------------------------------------------
# 指定したColumnの値を指定して行を削除 > Column=name Value=5 > 指定の行を抜き出す

    def deleteRecordsByCol(self, col: str, value: Any):
        deleteRow = self.getRowRecordsByCol(col=col, value=value)
        self.logger.warning(f"削除対象のデータです\n{deleteRow}")
        sql = f"DELETE FROM {self.fileName} WHERE {col} = ?"
        self.SQLPromptBase(sql=sql, params=(value, ), fetch=None)
        return self.logger.info(f"【success】{self.fileName} 指定のデータを削除")



# ----------------------------------------------------------------------------------