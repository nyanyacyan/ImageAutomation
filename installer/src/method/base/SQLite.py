# coding: utf-8
# $$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$
# テストOK
# $$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$
# import
import sqlite3
from typing import Any
from pathlib import Path
from datetime import datetime
from typing import Literal


# 自作モジュール
from .utils import Logger
from .path import BaseToPath
from .errorHandlers import NetworkHandler
from .decorators import Decorators
from ..const import Extension
from ..constSqliteTable import TableSchemas

decoInstance = Decorators(debugMode=True)


# $$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$
# **********************************************************************************
# 一連の流れ

class SQLite:
    def __init__(self, tableName: str, debugMode=True):

        # logger
        self.getLogger = Logger(__name__, debugMode=debugMode)
        self.logger = self.getLogger.getLogger()

        self.tableName = tableName

        # インスタンス化
        self.networkError = NetworkHandler(debugMode=debugMode)
        self.path = BaseToPath(debugMode=debugMode)
        self.currentDate = datetime.now().strftime('%y%m%d')
        self.tablePattern = TableSchemas.TABLE_PATTERN


# ----------------------------------------------------------------------------------
# ①

    def boolFilePath(self, extension: str = Extension.DB.value):
        dbDirPath = self.path.getResultDBDirPath()
        self.logger.warning(f"dbDirPath: {dbDirPath}")
        dbFilePath = dbDirPath / f"{self.currentDate}{extension}"
        if dbFilePath.exists():
            self.logger.warning(f"ファイルが見つかりました: {dbFilePath}")
            return True
        else:
            self.logger.warning(f"ファイルが見つかりません: {dbFilePath}")
            return False


# ----------------------------------------------------------------------------------
# # ①

    def DBFullPath(self, extension: str = Extension.DB.value):
        dbDirPath = self.path.getResultDBDirPath()
        dbFilePath = dbDirPath / f"{self.currentDate}{extension}"
        return dbFilePath


# ----------------------------------------------------------------------------------
# ②
# ディレクトリがない可能性の箇所に貼る関数→同時にテーブルを作成

    def isFileExists(self):
        fullPath = self.DBFullPath()

        if not fullPath.exists():
            fullPath.touch()
            self.logger.info(f"{fullPath.name} がないため作成")
        else:
            self.logger.debug(f"{fullPath.name} 発見")
        return fullPath


# ----------------------------------------------------------------------------------
# ③
# SQLiteにcookiesの情報を書き込めるようにするための初期設定

    @decoInstance.funcBase
    def createAllTable(self):
        for tableName, cols in self.tablePattern.items():
            self.logger.debug(f"tableName: {tableName}")
            sql = self.createTableSqlPrompt(tableName=tableName, cols=cols)
            self.SQLPromptBase(sql=sql)
            self.checkTableExists(tableName=tableName)


# ----------------------------------------------------------------------------------
# ④

    @decoInstance.funcBase
    def createTableSqlPrompt(self, tableName: str, cols: dict):
        colDef = ',\n'.join([f"{colName} {colSTS}" for colName, colSTS in cols.items()])
        self.logger.debug(f"colDef: {colDef}")

        prompt = f"CREATE TABLE IF NOT EXISTS {tableName}(\n{colDef}\n)"
        return prompt


# ----------------------------------------------------------------------------------
#TODO 現在使われてない


    def checkAllTablesExist(self, tablePattern: dict):
        for tableName in tablePattern.keys():
            exists = self._tableExists(tableName=tableName)
            if exists:
                self.logger.info(f"{tableName} は存在してます")
            else:
                self.logger.error(f"{tableName} が存在しません")


# ----------------------------------------------------------------------------------
#TODO 現在使われてない


    @decoInstance.funcBase
    def _tableExists(self, tableName: str):
        sql = "SELECT name FROM sqlite_master WHERE type='table';"
        tablesData = self.SQLPromptBase(sql=sql, fetch='all')
        tableNames = [tableData[0] for tableData in tablesData]
        self.logger.critical(f"tableNames: {tableNames}")

        self.logger.critical(f"tableNames:\n{tableNames}")
        if tableName in tableNames:
            self.logger.info(f"【success】{tableName} tableDataは存在してます")
            return True
        else:
            self.logger.error(f"【success】{tableName} tableDataが存在しません")
            return False


# ----------------------------------------------------------------------------------
# # params: tuple = () > パラメータが何もなかったら空にするという意味

    @decoInstance.sqliteHandler
    def SQLPromptBase(self, sql: str, params: tuple = (), fetch: str = None):
        conn = self._getDBconnect()
        if not conn:
            return None

        try:
            cursor = self._executeSQL(conn=conn, sql=sql, params=params)
            result = self._fetchBool(cursor=cursor, fetch=fetch)
            return result

        finally:
            self.logger.debug("connを閉じました")
            conn.close()


# ----------------------------------------------------------------------------------
# 実行するSQL文にて定義して実行まで行う

    @decoInstance.sqliteHandler
    def _executeSQL(self, conn: sqlite3.Connection, sql: str, params: tuple = ()) -> sqlite3.Cursor:
        cursor = conn.cursor()  # DBとの接続オブジェクトを受け取って通信ができるようにする
        cursor.execute(sql, params)  # 実行するSQL文にて定義して実行まで行う
        return cursor


# ----------------------------------------------------------------------------------
# fetchの属性をキャッチ

    @decoInstance.sqliteHandler
    def _fetchBool(self, cursor: sqlite3.Cursor, fetch: Literal['one', 'all', None]):
        if fetch == 'one':
            self.logger.debug(f"[one] c.fetchone()が実行されました")
            return cursor.fetchone()

        elif fetch == 'all':
            self.logger.debug(f"[all] c.fetchall()が実行されました")
            return cursor.fetchall()

        # データ抽出以外の処理を実施した場合
        else:
            cursor.connection.commit()
            self.logger.info(f"コミットの実施をしました")
            return None


# ----------------------------------------------------------------------------------


    @decoInstance.sqliteHandler
    def _getDBconnect(self) -> sqlite3.Connection:
        dbFullPath = self.DBFullPath()
        return sqlite3.connect(dbFullPath)


# ----------------------------------------------------------------------------------


    @decoInstance.funcBase
    def resetTable(self):
        self.logger.warning("既存のテーブルを破棄して、再度構築")
        sqlDrop = f"DROP TABLE IF EXISTS {self.tableName}"
        self.SQLPromptBase(sql=sqlDrop, fetch=None)
        return self.createTable()


# ----------------------------------------------------------------------------------
# テーブルのすべてのカラムを取得する
# PRAGMA table_infoはそのテーブルのColumn情報を取得する
# →1つ目のリストはcolumnID、２つ目column名、３つ目データ型、４つ目はカラムがNULLを許可するかどうかを示す（1はNOT NULL、0はNULL許可）
# ５→columnに指定されたデフォルト値
# columnData[1]=columns名

    @decoInstance.funcBase
    def columnsExists(self, tableName: str):
        sql = f"PRAGMA table_info({tableName});"
        columnsStatus = self.SQLPromptBase(sql=sql, fetch='all')
        self.logger.warning(f"columnsStatus: {columnsStatus}")

        columnNames = [columnData[1] for columnData in columnsStatus]
        self.logger.info(f"columnNames: {columnNames}")
        return columnNames


# ----------------------------------------------------------------------------------


    @decoInstance.funcBase
    def checkTableExists(self, tableName: str):
        sql = f"SELECT name FROM sqlite_master WHERE type='table';"
        result = self.SQLPromptBase(sql=sql, fetch='all')
        self.logger.warning(f"result: {result}")

        tableNames = [table[0] for table in result]
        self.logger.critical(f"tableNames: {tableNames}")
        if tableName in tableNames:
            self.logger.info(f"{tableName} テーブルの作成に成功しています。")
        else:
            self.logger.error(f"{tableName} テーブルの作成に失敗してます")
        return result


# ----------------------------------------------------------------------------------
# SQLiteへ入れ込む

    @decoInstance.funcBase
    def insertData(self, col: tuple, values: tuple):
        placeholders = ', '.join(['?' for _ in values]) # valuesの数の文？を追加して結合
        self.logger.warning(f"values: {values}")
        sql = f"INSERT INTO {self.tableName} {col} VALUES ({placeholders})"
        rowData = self.SQLPromptBase(sql=sql, params=values, fetch=None)
        self.logger.warning(f"{self.tableName} の行データ: {rowData}")
        self.logger.info(f"【success】{self.tableName} テーブルにデータを追加に成功")

        sqlCheck = f"SELECT * FROM {self.tableName}"
        allData = self.SQLPromptBase(sql=sqlCheck, fetch='all')
        self.logger.warning(f"{self.tableName} の全データ: {allData}")
        return rowData


# ----------------------------------------------------------------------------------
# テーブルデータを全て引っ張る

    @decoInstance.funcBase
    def getRecordsAllData(self):
        sql = f"SELECT * FROM {self.tableName}"
        result = self.SQLPromptBase(sql=sql, fetch='all')
        self.logger.info(f"【success】{self.tableName} すべてのデータを抽出")
        self.logger.info(f"result: {result}")
        return result


# ----------------------------------------------------------------------------------
# 指定したColumnの値を指定して行を抽出 > Column=name Value=5 > 指定の行を抜き出す > List

    @decoInstance.funcBase
    def getAllRecordsByCol(self, col: str, value: Any):
        sql = f"SELECT * FROM {self.tableName} WHERE {col} = ?"
        result = self.SQLPromptBase(sql=sql, params=(value, ), fetch='all')
        self.logger.info(f"【success】{self.tableName} 指定のカラムデータをすべて抽出")
        self.logger.info(f"result: {result}")
        return result


# ----------------------------------------------------------------------------------
# 指定したColumnの値を指定して行を抽出 > Column=name Value=5 > 指定の行を抜き出す > row

    @decoInstance.funcBase
    def getRowRecordsByCol(self, col: str, value: Any):
        sql = f"SELECT * FROM {self.tableName} WHERE {col} = ?"
        result = self.SQLPromptBase(sql=sql, params=(value, ), fetch='one')
        if result:
            self.logger.info(f"【success】{self.tableName} 指定の行のデータを抽出")
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
        sql = f"DELETE FROM {self.tableName} WHERE {col} = ?"
        result = self.SQLPromptBase(sql=sql, params=(value, ), fetch=None)
        self.logger.info(f"【success】{self.tableName} 指定のデータを削除")
        self.logger.info(f"result: {result}")
        return result


# ----------------------------------------------------------------------------------
# 指定したColumnの値を指定して行を削除 > Column=name Value=5 > 指定の行を抜き出す

    @decoInstance.funcBase
    def deleteAllRecords(self):
        deleteData = self.getRecordsAllData()
        self.logger.warning(f"削除対象のデータです\n{deleteData}")
        sql = f"DELETE FROM {self.tableName}"
        result = self.SQLPromptBase(sql=sql, fetch=None)
        self.logger.info(f"【success】{self.tableName} すべてのデータを削除")
        self.logger.info(f"result: {result}")
        return result


# ----------------------------------------------------------------------------------