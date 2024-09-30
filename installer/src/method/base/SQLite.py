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
from .decorators import Decorators

decoInstance = Decorators(debugMode=True)


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
    @decoInstance.funcBase
    def startSQLPromptBase(self, sql: str, params: tuple = (), fetch: str = None):
        conn = self.getDBconnect()
        try:
            c = conn.cursor()  # DBとの接続オブジェクトを受け取って通信ができるようにする
            self.logger.debug(f"SQL実行: {sql}, パラメータ: {params}")
            c.execute(sql, params)  # 実行するSQL文にて定義して実行まで行う

            self.logger.info(f"[success]テーブルは存在してることを確認")

            if fetch == 'all':
                self.logger.debug(f"[all] c.fetchall()が実行されました")
                return c.fetchall()

        except sqlite3.OperationalError as e:
            if 'no such table' in str(e):
                self.logger.warning(f"テーブルが存在しません: {e}")
                return self.createTable()

        except Exception as e:
            conn.rollback()
            self.logger.error(f"エラーが発生しました。トランザクションをロールバックしました:{e}")  # ロールバックは変更する前の状態に戻すこと

        finally:
            self.logger.warning("connを閉じました")
            conn.close()

# ----------------------------------------------------------------------------------
# 指定したColumnの値を指定して行を抽出 > Column=name Value=5 > 指定の行を抜き出す > List

    @decoInstance.funcBase
    def startGetAllRecordsByCol(self):
        sqlCheck = f"SELECT * FROM {self.fileName}"
        result = self.startSQLPromptBase(sql=sqlCheck, fetch='all')
        self.logger.info(f"【success】{self.fileName} 指定のカラムデータをすべて抽出")
        self.logger.info(f"result: {result}")
        return result


# ----------------------------------------------------------------------------------
# # params: tuple = ()　> パラメータが何もなかったら空にするという意味
    @decoInstance.funcBase
    def SQLPromptBase(self, sql: str, params: tuple = (), fetch: str = None):
        conn = self.getDBconnect()
        try:
            c = conn.cursor()  # DBとの接続オブジェクトを受け取って通信ができるようにする
            self.logger.debug(f"SQL実行: {sql}, パラメータ: {params}")
            c.execute(sql, params)  # 実行するSQL文にて定義して実行まで行う

            if fetch == 'one':
                self.logger.debug(f"[all] c.fetchall()が実行されました")
                return c.fetchone()
            elif fetch == 'all':
                self.logger.debug(f"[all] c.fetchall()が実行されました")
                return c.fetchall()
            else:
                conn.commit()
                self.logger.warning("コミットの実施を行いました")
                return None

        except sqlite3.OperationalError as e:
            if 'no such table' in str(e):
                self.logger.error(f"テーブルは作成されてるはずなのにない: {e}")
                raise Exception("テーブルの作成が完了してるはずができてない")


        except Exception as e:
            conn.rollback()
            self.logger.error(f"エラーが発生しました。トランザクションをロールバックしました:{e}")  # ロールバックは変更する前の状態に戻すこと

        finally:
            self.logger.warning("connを閉じました")
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

    @decoInstance.funcBase
    def createTable(self):
        self.logger.warning(f"self.fileName: {self.fileName}")
        sql = f'''
            CREATE TABLE IF NOT EXISTS {self.fileName} (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
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
        self.checkTableExists()


# ----------------------------------------------------------------------------------

    @decoInstance.funcBase
    def resetTable(self):
        self.logger.warning("既存のテーブルを破棄して、再度構築")
        sqlDrop = f"DROP TABLE IF EXISTS {self.fileName}"
        self.SQLPromptBase(sql=sqlDrop, fetch=None)
        return self.createTable()


# ----------------------------------------------------------------------------------
    @decoInstance.funcBase
    def checkTableExists(self):
        sql = f"SELECT name FROM sqlite_master WHERE type='table';"
        result = self.SQLPromptBase(sql=sql, fetch='all')
        self.logger.warning(f"result: {result}")
        if result:
            self.logger.info(f"{self.fileName} テーブルの作成に成功しています。")
        else:
            self.logger.error(f"{self.fileName} テーブルの作成に失敗してます")
        return result



# ----------------------------------------------------------------------------------
# SQLiteへ入れ込む

    @decoInstance.funcBase
    def insertData(self, col: tuple, values: tuple):
        placeholders = ', '.join(['?' for _ in values]) # valuesの数の文？を追加して結合
        self.logger.warning(f"values: {values}")
        sql = f"INSERT INTO {self.fileName} {col} VALUES ({placeholders})"
        rowData = self.SQLPromptBase(sql=sql, params=values, fetch=None)
        self.logger.warning(f"{self.fileName} の行データ: {rowData}")
        self.logger.info(f"【success】{self.fileName} テーブルにデータを追加に成功")

        sqlCheck = f"SELECT * FROM {self.fileName}"
        allData = self.SQLPromptBase(sql=sqlCheck, fetch='all')
        self.logger.warning(f"{self.fileName} の全データ: {allData}")
        return rowData


# ----------------------------------------------------------------------------------
# テーブルデータを全て引っ張る

    @decoInstance.funcBase
    def getRecordsAllData(self):
        sql = f"SELECT * FROM {self.fileName}"
        result = self.SQLPromptBase(sql=sql, fetch='all')
        self.logger.info(f"【success】{self.fileName} すべてのデータを抽出")
        self.logger.info(f"result: {result}")
        return result


# ----------------------------------------------------------------------------------
# 指定したColumnの値を指定して行を抽出 > Column=name Value=5 > 指定の行を抜き出す > List

    @decoInstance.funcBase
    def getAllRecordsByCol(self, col: str, value: Any):
        sql = f"SELECT * FROM {self.fileName} WHERE {col} = ?"
        result = self.SQLPromptBase(sql=sql, params=(value, ), fetch='all')
        self.logger.info(f"【success】{self.fileName} 指定のカラムデータをすべて抽出")
        self.logger.info(f"result: {result}")
        return result


# ----------------------------------------------------------------------------------
# 指定したColumnの値を指定して行を抽出 > Column=name Value=5 > 指定の行を抜き出す > row

    @decoInstance.funcBase
    def getRowRecordsByCol(self, col: str, value: Any):
        sql = f"SELECT * FROM {self.fileName} WHERE {col} = ?"
        result = self.SQLPromptBase(sql=sql, params=(value, ), fetch='one')
        if result:
            self.logger.info(f"【success】{self.fileName} 指定の行のデータを抽出")
            self.logger.info(f"result: {result}")
            return result
        else:
            self.logger.error(f"resultがNoneです。命令文に問題がある可能性があります")


# ----------------------------------------------------------------------------------
# 指定したColumnの値を指定して行を削除 > Column=name Value=5 > 指定の行を抜き出す

    @decoInstance.funcBase
    def deleteRecordsByCol(self, col: str, value: Any):
        deleteRow = self.getRowRecordsByCol(col=col, value=value)
        self.logger.warning(f"削除対象のデータです\n{deleteRow}")
        sql = f"DELETE FROM {self.fileName} WHERE {col} = ?"
        result = self.SQLPromptBase(sql=sql, params=(value, ), fetch=None)
        self.logger.info(f"【success】{self.fileName} 指定のデータを削除")
        self.logger.info(f"result: {result}")
        return result


# ----------------------------------------------------------------------------------
# 指定したColumnの値を指定して行を削除 > Column=name Value=5 > 指定の行を抜き出す

    @decoInstance.funcBase
    def deleteAllRecords(self):
        deleteData = self.getRecordsAllData()
        self.logger.warning(f"削除対象のデータです\n{deleteData}")
        sql = f"DELETE FROM {self.fileName}"
        result = self.SQLPromptBase(sql=sql, fetch=None)
        self.logger.info(f"【success】{self.fileName} すべてのデータを削除")
        self.logger.info(f"result: {result}")
        return result


# ----------------------------------------------------------------------------------