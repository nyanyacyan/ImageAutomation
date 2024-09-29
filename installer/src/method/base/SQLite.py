# coding: utf-8
# $$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$
# テストOK
# $$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$
# import
import sqlite3
from functools import wraps
from typing import Any


# 自作モジュール
from .utils import Logger
from .path import BaseToPath
from ..const import SubDir
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

    def createCookieDB(self):
        conn = self.getDBconnect()
        try:
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

            c = conn.cursor()  # DBとの接続オブジェクトを受け取って通信ができるようにする

            c.execute(sql)  # 実行するSQL文にて定義して実行まで行う

        except Exception as e:
            conn.rollback()
            self.logger.error(f"エラーが発生しました。トランザクションをロールバックしました:{e}")  # ロールバックは変更する前の状態に戻すこと
            raise e
        finally:
            conn.close()



# ----------------------------------------------------------------------------------
# SQLiteへ入れ込む

    def insertTable(self, col: tuple, values: tuple):
        conn = self.getDBconnect()
        try:
            placeholders = ', '.join(['?' for _ in values]) # valuesの数の文？を追加して結合
            sql = f"INSERT INTO {self.fileName} {col} VALUES {placeholders}"

            c = conn.cursor()
            c.execute(sql, values)

        except Exception as e:
            conn.rollback()
            self.logger.error(f"エラーが発生しました。トランザクションをロールバックしました:{e}")  # ロールバックは変更する前の状態に戻すこと
            raise e
        finally:
            conn.close()


# ----------------------------------------------------------------------------------
# テーブルデータを全て引っ張る

    def getRecordsAllData(self):
        conn = self.getDBconnect()
        try:
            sql = f"SELECT * FROM {self.fileName}"

            c = conn.cursor()
            c.execute(sql)
            return c.fetchall()

        except Exception as e:
            conn.rollback()
            self.logger.error(f"エラーが発生しました。トランザクションをロールバックしました:{e}")  # ロールバックは変更する前の状態に戻すこと
            raise e
        finally:
            conn.close()


# ----------------------------------------------------------------------------------
# 指定したColumnの値を指定して行を抽出 > Column=name Value=5 > 指定の行を抜き出す > List

    def getAllRecordsByCol(self, col: str, value: Any):
        conn = self.getDBconnect()
        try:
            sql = f"SELECT * FROM {self.fileName} WHERE {col} = ?"

            c = conn.cursor()
            c.execute(sql, (value,))
            return c.fetchall()

        except Exception as e:
            conn.rollback()
            self.logger.error(f"エラーが発生しました。トランザクションをロールバックしました:{e}")  # ロールバックは変更する前の状態に戻すこと
            raise e
        finally:
            conn.close()


# ----------------------------------------------------------------------------------
# 指定したColumnの値を指定して行を抽出 > Column=name Value=5 > 指定の行を抜き出す > row

    def getRowRecordsByCol(self, col: str, value: Any):
        conn = self.getDBconnect()
        try:
            sql = f"SELECT * FROM {self.fileName} WHERE {col} = ?"

            c = conn.cursor()
            c.execute(sql, (value,))
            return c.fetchone()

        except Exception as e:
            conn.rollback()
            self.logger.error(f"エラーが発生しました。トランザクションをロールバックしました:{e}")  # ロールバックは変更する前の状態に戻すこと
            raise e
        finally:
            conn.close()


# ----------------------------------------------------------------------------------
# 指定したColumnの値を指定して行を削除 > Column=name Value=5 > 指定の行を抜き出す

    def deleteRecordsByCol(self, col: str, value: Any):
        try:
            conn = self.getDBconnect()
            deleteRow = self.getRecordsByCol(conn=conn, col=col, value=value)
            self.logger.warning(f"削除対象のデータです\n{deleteRow}")
            sql = f"DELETE FROM {self.fileName} WHERE {col} = ?"

            c = conn.cursor()
            c.execute(sql, (value,))

        except Exception as e:
            conn.rollback()
            self.logger.error(f"エラーが発生しました。トランザクションをロールバックしました:{e}")  # ロールバックは変更する前の状態に戻すこと
            raise e
        finally:
            conn.close()


# ----------------------------------------------------------------------------------