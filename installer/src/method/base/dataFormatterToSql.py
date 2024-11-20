# coding: utf-8
# $$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$
# 2024/9/23 更新

# sudo tree /Users/nyanyacyan/Desktop/Project_file/SNS_auto_upper -I 'venv|pyvenv.cfg|__pycache__'


# $$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$
# import
import os
from typing import List

# 自作モジュール
from base.utils import Logger
from installer.src.method.base.insertSql import DataInSQLite
from base.textManager import TextManager


# $$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$

# **********************************************************************************
# 一連の流れ

class DataFormatterToSql:
    def __init__(self, debugMode=True):

        # logger
        self.getLogger = Logger(__name__, debugMode=debugMode)
        self.logger = self.getLogger.getLogger()

        self.dataInSQLite = DataInSQLite(chrome=self.chrome, debugMode=debugMode)
        self.textManager = TextManager(debugMode=debugMode)


# ----------------------------------------------------------------------------------
# 各データをパターンごとにまとめる辞書

    def allDataCreate(self):
        data = {
            'A': self.dataA_create(),
            'B': self.dataC_create(),
            'C': self.dataC_create(),
            'D': self.dataD_create()
        }

        return data

# ----------------------------------------------------------------------------------
# TODO データ型に入れ込む

    def dataA_create(self):
        pass
        data_A = {
            'imagePath_1': '',
            'text_1': '',
            'text_2': '',
            'text_3': ''
        }


# ----------------------------------------------------------------------------------


    def dataB_create(self):
        pass
        data_B = {
            'imagePath_1': '',
            'imagePath_2': '',
            'text_1': '',
            'text_2': '',
            'text_3': ''
        }


# ----------------------------------------------------------------------------------


    def dataC_create(self):
        pass
        data_C = {
            'imagePath_1': '',
            'imagePath_2': '',
            'text_1': '',
            'text_2': ''
        }


# ----------------------------------------------------------------------------------


    def dataD_create(self):
        pass
        data_D = {
            'imagePath_1': '',
            'imagePath_2': '',
            'text_1': '',
            'text_2': ''
        }


# ----------------------------------------------------------------------------------
# TODO SQLiteからのテキストデータを加工する（結合）
# TODO 駅名と徒歩
# TODO 専有面積とselectItem[0]~[3]
# TODO selectItem[4]~[7]
# TODO selectItem[8]~[11]


# ----------------------------------------------------------------------------------
# データ結合

    def textJoin(self, joinWordsList: List, joint: str):
        return self.textManager.textJoin(joinWordsList=joinWordsList, joint=joint)


# ----------------------------------------------------------------------------------
# TODO SQLiteデータを文字列からデータがへ変換


# ----------------------------------------------------------------------------------
# ----------------------------------------------------------------------------------
# ----------------------------------------------------------------------------------
