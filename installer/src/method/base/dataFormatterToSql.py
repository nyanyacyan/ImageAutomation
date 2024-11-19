# coding: utf-8
# $$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$
# 2024/9/23 更新

# sudo tree /Users/nyanyacyan/Desktop/Project_file/SNS_auto_upper -I 'venv|pyvenv.cfg|__pycache__'


# $$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$
# import
import os

# 自作モジュール
from base.utils import Logger
from base.dataInSqlite import DataInSQLite


# $$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$

# **********************************************************************************
# 一連の流れ

class DataFormatterToSql:
    def __init__(self, debugMode=True):

        # logger
        self.getLogger = Logger(__name__, debugMode=debugMode)
        self.logger = self.getLogger.getLogger()

        self.dataInSQLite = DataInSQLite(chrome=self.chrome, debugMode=debugMode)



# ----------------------------------------------------------------------------------
# TODO データ型に入れ込む


data_A = {
    'imagePath_1': '',
    'text_1': '',
    'text_2': '',
    'text_3': ''
}

data_B = {
    'imagePath_1': '',
    'imagePath_2': '',
    'text_1': '',
    'text_2': '',
    'text_3': ''
}

data_C = {
    'imagePath_1': '',
    'imagePath_2': '',
    'text_1': '',
    'text_2': ''
}

data_D = {
    'imagePath_1': '',
    'imagePath_2': '',
    'text_1': '',
    'text_2': ''
}

# 各データをパターンごとにまとめる辞書
data = {
    'A': data_A,
    'B': data_B,
    'C': data_C,
    'D': data_D
}



# ----------------------------------------------------------------------------------
# TODO SQLiteからのテキストデータを加工する（結合）
# TODO 駅名と徒歩
# TODO 専有面積とselectItem[0]~[3]
# TODO selectItem[4]~[7]
# TODO selectItem[8]~[11]


# ----------------------------------------------------------------------------------
# TODO SQLiteデータを文字列からデータがへ変換


# ----------------------------------------------------------------------------------
# ----------------------------------------------------------------------------------
# ----------------------------------------------------------------------------------
