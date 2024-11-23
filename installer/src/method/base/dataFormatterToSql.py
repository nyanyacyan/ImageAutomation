# coding: utf-8
# $$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$
# 2024/9/23 更新

# sudo tree /Users/nyanyacyan/Desktop/Project_file/SNS_auto_upper -I 'venv|pyvenv.cfg|__pycache__'


# $$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$
# import
import os
from typing import List, Dict
from selenium.webdriver.chrome.webdriver import WebDriver


# 自作モジュール
from base.utils import Logger
from base.insertSql import InsertSql
from base.textManager import TextManager
from constSqliteTable import TableSchemas
from base.imageEditor import ImageEditor


# $$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$

# **********************************************************************************
# 一連の流れ

class DataFormatterToSql:
    def __init__(self, chrome: WebDriver, debugMode=True):

        # logger
        self.getLogger = Logger(__name__, debugMode=debugMode)
        self.logger = self.getLogger.getLogger()

        self.chrome = chrome

        self.insertSql = InsertSql(chrome=self.chrome, debugMode=debugMode)
        self.textManager = TextManager(debugMode=debugMode)
        self.imageEditor = ImageEditor(debugMode=debugMode)


# ----------------------------------------------------------------------------------
# 各データをパターンごとにまとめる辞書

    def flowAllDataCreate(self, allDataDict: Dict):
        self.logger.info(f"すべてのデータ数: {len(allDataDict)}")
        self.logger.debug(f"allDataDict: {allDataDict}")
        for key, valueDict in allDataDict.items():
            self.logger.warning(f"key: {key}\nvalueDict: {valueDict}")
            dataDict, fileName, ad = self.allDataCreate(dataDict=valueDict)
            self.imageEditor.executePatternEditors(dataDict=dataDict, buildingName=fileName)

            # TODO adのリストを作成


# ----------------------------------------------------------------------------------
# 各データをパターンごとにまとめる辞書

    def allDataCreate(self, dataDict: Dict):
        print(f"dataDict: {dataDict}")
        fileName = dataDict['text']['name']
        print(f"fileName: {fileName}")
        ad = dataDict['text']['ad']
        data = {
            'A': self.dataA_create(dataDict),
            'B': self.dataB_create(dataDict),
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

        self.logger.warning(f"\nimageData: {imageData}\ntext_2: {text_2}\ntext_3: {text_3}")

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
        text_1 = self._dataB_text_1(dataDict=textDataDict)
        text_2 = textDataDict['secondComment']
        text_3 = self._formatDepositTotal(dataDict=textDataDict)

        self.logger.warning(f"\nimageData: {imageData}\ntext_2: {text_2}\ntext_3: {text_3}")


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
        text_1 = self._data_C_D_text_1(dataDict=textDataDict, startNum=3, endNum=8)
        text_2 = textDataDict['thirdComment']

        self.logger.warning(f"\nimageData: {imageData}\ntext_2: {text_2}")


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
        text_1 = self._data_C_D_text_1(dataDict=textDataDict, startNum=8, endNum=12)
        text_2 = textDataDict['fourthComment']

        self.logger.warning(f"\nimageData: {imageData}\ntext_2: {text_2}")


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
        keyValues = [[key, dataDict[key]] for key in priorityList if key in dataDict and dataDict[key]]
        keyValues = keyValues[:maxlen]
        for i, (key, value) in enumerate(keyValues):
            self.logger.info(f"優先度を反映したデータ {i + 1} 個目のデータを選出:\nkey:{key}\nvalue:{value}")
        values = [value for _, value in keyValues]
        return values


# ----------------------------------------------------------------------------------
# 専有面積とselectItem[0]~[3]

    def _dataB_text_1(self, dataDict: Dict, startNum: int = 0, endNum: int = 4):
        area = '専有面積' + dataDict['area']
        items = dataDict['selectItems'][startNum:endNum]
        print(f"items: {items}")
        result = f"・{area}\n\n・{items[0]}\n\n・{items[1]}\n\n・{items[2]}\n\n・{items[3]}"
        print(f"text_1: {result}")
        return result


# ----------------------------------------------------------------------------------
# dataC~Dのtext_1

    def _data_C_D_text_1(self, dataDict: Dict, startNum: int, endNum: int):
        print(f"dataDict: {dataDict}")
        print(f"selectItems: {dataDict['selectItems']}")
        items = dataDict['selectItems'][startNum:endNum]
        result = f"・{items[0]}\n\n・{items[1]}\n\n・{items[2]}\n\n・{items[3]}"
        print(f"text_1: {result}")
        return result


# ----------------------------------------------------------------------------------
# 敷金礼金

    def _formatDepositTotal(self, dataDict: Dict):
        rent_str = dataDict['rent']
        deposit_str = dataDict['deposit']
        keyMoney_str = dataDict['keyMoney']

        rent = self._int_to_Str(rent_str)
        deposit = self._int_to_Str(deposit_str)
        keyMoney = self._int_to_Str(keyMoney_str)

        total = rent * (deposit + keyMoney)

        depositTotal = f"敷金 {rent_str}  礼金 {keyMoney_str}  合計 {total} 円"
        self.logger.debug(f"敷金礼金の文言: {depositTotal}")
        return depositTotal

# ----------------------------------------------------------------------------------
# テキストから数値を抜き出す

    def _int_to_Str(self, strData: str):
        number = int(''.join(filter(str.isdigit, strData)))
        self.logger.info(f"文字列から数値に変換: {number}")
        return number


# ----------------------------------------------------------------------------------
# TODO adのリストを作成





# ----------------------------------------------------------------------------------
# データ結合

    def textJoin(self, joinWordsList: List, joint: str):
        return self.textManager.textJoin(joinWordsList=joinWordsList, joint=joint)


# ----------------------------------------------------------------------------------
# TODO SQLiteデータを文字列からデータがへ変換






# ----------------------------------------------------------------------------------
# ----------------------------------------------------------------------------------
