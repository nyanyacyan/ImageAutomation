# coding: utf-8
# $$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$
# 2024/9/23 更新

# sudo tree /Users/nyanyacyan/Desktop/Project_file/SNS_auto_upper -I 'venv|pyvenv.cfg|__pycache__'


# $$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$
# import
import os
from typing import List, Dict

# 自作モジュール
from base.utils import Logger
from installer.src.method.base.insertSql import InsertSql
from base.textManager import TextManager
from constSqliteTable import TableSchemas
from imageEditor import ImageEditor


# $$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$

# **********************************************************************************
# 一連の流れ

class DataFormatterToSql:
    def __init__(self, debugMode=True):

        # logger
        self.getLogger = Logger(__name__, debugMode=debugMode)
        self.logger = self.getLogger.getLogger()

        self.insertSql = InsertSql(chrome=self.chrome, debugMode=debugMode)
        self.textManager = TextManager(debugMode=debugMode)
        self.imageEditor = ImageEditor(debugMode=debugMode)


# ----------------------------------------------------------------------------------
# 各データをパターンごとにまとめる辞書

    def allDataCreate(self, allDataDict: Dict):
        self.logger.info(f"すべてのデータ数: {len(allDataDict)}")
        for dataDict in allDataDict:
            dataDict, fileName, ad = self.allDataCreate(dataDict=dataDict)
            self.imageEditor.executePatternEditors(dataDict=dataDict, buildingName=fileName)

            # TODO adのリストを作成
            

# ----------------------------------------------------------------------------------
# 各データをパターンごとにまとめる辞書

    def allDataCreate(self, dataDict: Dict):
        fileName = dataDict['name']
        ad = dataDict['ad']
        data = {
            'A': self.dataA_create(dataDict),
            'B': self.dataC_create(dataDict),
            'C': self.dataC_create(dataDict),
            'D': self.dataD_create(dataDict)
        }

        return fileName, data, ad

# ----------------------------------------------------------------------------------
# TODO データ型に入れ込む

    def dataA_create(self, dataDict: Dict):
        # 写真データ
        imageData = dataDict['image']['外観']

        # テキストデータ
        textDataDict = dataDict['text']
        print(f"textDataDict: {textDataDict}")
        text_2 = textDataDict['trainName']
        text_3 = textDataDict['stationWord']

        data_A = {
            'imagePath_1': imageData,
            'text_1': '物件情報',
            'text_2': text_2,
            'text_3': text_3
        }

        return data_A


# ----------------------------------------------------------------------------------


    def dataB_create(self, dataDict: Dict):
        # 写真データ
        imageData = dataDict['image']
        priorityOrder = TableSchemas.IMAGE_PRIORITY_2

        # 優先度を優先したデータ
        imageUrlList = self._priorityData(dataDict=imageData, priorityList=priorityOrder)

        # テキストデータ
        textDataDict = dataDict['text']
        print(f"textDataDict: {textDataDict}")
        text_1 = textDataDict['']
        text_2 = textDataDict['secondComment']
        text_3 = textDataDict['']


        data_B = {
            'imagePath_1': imageUrlList[0] if len(imageUrlList) > 0 else None,
            'imagePath_2': imageUrlList[1] if len(imageUrlList) > 1 else None,
            'text_1': text_1,
            'text_2': text_2,
            'text_3': text_3,
        }

        return data_B


# ----------------------------------------------------------------------------------


    def dataC_create(self, dataDict: Dict, imageNum: int = 2):
        # 写真データ
        imageData = dataDict['image']
        priorityOrder = TableSchemas.IMAGE_PRIORITY_2

        # 優先度を優先したデータ
        imageUrlList = self._priorityData(dataDict=imageData, priorityList=priorityOrder)

        # テキストデータ
        textDataDict = dataDict['text']
        print(f"textDataDict: {textDataDict}")
        text_1 = textDataDict['']
        text_2 = textDataDict['thirdComment']

        data_C = {
            'imagePath_1': imageUrlList[0] if len(imageUrlList) > 0 else None,
            'imagePath_2': imageUrlList[1] if len(imageUrlList) > 1 else None,
            'text_1': text_1,
            'text_2': text_2
        }
        return data_C


# ----------------------------------------------------------------------------------


    def dataD_create(self, dataDict: Dict):
        # 写真データ
        imageData = dataDict['image']
        priorityOrder = TableSchemas.IMAGE_PRIORITY_2

        # 優先度を優先したデータ
        imageUrlList = self._priorityData(dataDict=imageData, priorityList=priorityOrder)

        # テキストデータ
        textDataDict = dataDict['text']
        print(f"textDataDict: {textDataDict}")
        text_1 = textDataDict['']
        text_2 = textDataDict['fourthComment']


        data_D = {
            'imagePath_1': imageUrlList[0] if len(imageUrlList) > 0 else None,
            'imagePath_2': imageUrlList[1] if len(imageUrlList) > 1 else None,
            'text_1': text_1,
            'text_2': text_2
        }

        return data_D


# ----------------------------------------------------------------------------------
# priority

    def _priorityData(self, dataDict: Dict, priorityList: List, maxlen: int = 3):
        values = [dataDict[key] for key in priorityList if key in dataDict and dataDict[key]]
        values = values[:maxlen]
        for i, value in enumerate(values):
            self.logger.info(f"優先度を反映したデータ {i + 1} 個目: {value}")
        return values


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
