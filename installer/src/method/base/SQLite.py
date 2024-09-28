# coding: utf-8
# $$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$
# テストOK
# $$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$
# import
import sqlite3
from functools import wraps


# 自作モジュール
from .utils import Logger
from .path import BaseToPath
from ..const import SubDir
from .errorHandlers import NetworkHandler


# $$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$
# **********************************************************************************
# 一連の流れ

class DecoSQLite:
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
        return self.path.getResultSubDirFilePath(subDirName=SubDir.DBSubDir.value, fileName=self.fileName)


# ----------------------------------------------------------------------------------


    def getDBConnection(self, dbFullPath: str):
        dbFullPath = self.getDBFullPath()
        return sqlite3.Connection(dbFullPath)


# ----------------------------------------------------------------------------------


    def transactional(self):
        def decorator(func):
            @wraps(func)
            def wrapper(*args, **kwargs):
                conn = self.getDBConnection()
                try:
                    result = func(conn, *args, **kwargs)
                    conn.commit()
                    self.logger.info("トランザクションに成功しました。変更が確定されました。")
                    return result
                except Exception as e:
                    conn.rollback()
                    self.logger.error(f"エラーが発生しました。トランザクションをロールバックしました:{e}")  # ロールバックは変更する前の状態に戻すこと
                    raise e
                finally:
                    conn.close()
            return wrapper
        return decorator


# ----------------------------------------------------------------------------------
# SQL文を挿入してDBを定義する

    @transactional
    def createTable(self, conn: sqlite3.Connection, sql: str):
        c = conn.cursor  # DBとの接続オブジェクトを受け取って通信ができるようにする

        c.execute(sql)  # 実行するSQL文にて定義して実行まで行う


# ----------------------------------------------------------------------------------