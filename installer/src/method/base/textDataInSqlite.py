# coding: utf-8
# $$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$

# $$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$
# import
from selenium.webdriver.chrome.webdriver import WebDriver
from datetime import datetime


# 自作モジュール
from .utils import Logger
from .elementManager import ElementManager


# $$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$
# **********************************************************************************


class TextDataInSQLite:
    def __init__(self, chrome: WebDriver, debugMode=True):
        # logger
        self.getLogger = Logger(__name__, debugMode=debugMode)
        self.logger = self.getLogger.getLogger()

        self.chrome = chrome
        self.currentDate = datetime.now().strftime('%y%m%d_%H%M%S')
        self.element = ElementManager(debugMode=debugMode)


# ----------------------------------------------------------------------------------


    def mergeDict(self, name: str):
        metaInfo = self._topPageInfo()
        topPageInfo = self._secondPageInfo()
        secondPageInfo = self._secondPageInfo()
        thirdPageInfo = self._thirdPageInfo()
        fourthPageInfo = self._fourthPageInfo()

        # サブ辞書の初期化
        dataDict = self.element._initDict(name=name)

        # 順番にサブ辞書を追加していく
        dataDictInMeta = self.element.updateSubDict(dictBox=dataDict, name=name, inputDict=metaInfo)
        dataDictInTop = self.element.updateSubDict(dictBox=dataDictInMeta, name=name, inputDict=topPageInfo)
        dataDictInSecond = self.element.updateSubDict(dictBox=dataDictInTop, name=name, inputDict=secondPageInfo)
        dataDictInThird = self.element.updateSubDict(dictBox=dataDictInSecond, name=name, inputDict=thirdPageInfo)
        result = self.element.updateSubDict(dictBox=dataDictInThird, name=name, inputDict=fourthPageInfo)

        return result


# ----------------------------------------------------------------------------------
# metaInfo

    def _metaInfo(self, **kwargs):
        pass





# ----------------------------------------------------------------------------------


    def _topPageInfo(self, **kwargs):
        trainLine = self.element._getAddress(by=kwargs['trainLineBy'], value=kwargs['trainLineValue'])
        station = self.element._getAddress(by=kwargs['stationBy'], value=kwargs['stationValue'])
        address = self.element._getAddress(by=kwargs['addressBy'], value=kwargs['addressValue'])
        walking = self.element._getAddress(by=kwargs['walkingBy'], value=kwargs['walkingValue'])

        dataDict = {
            "trainLine": trainLine,
            "station": station,  # 駅名
            "address": address,  # 都道府県
            "walking": walking,  # 徒歩
        }

        return dataDict



# ----------------------------------------------------------------------------------


    def _secondPageInfo(self, **kwargs):
        areaScale = self.getElement(by=kwargs['areaBy'], value=kwargs['areaValue'])
        itemList = self._textCleaner(by=kwargs['itemBy'], value=kwargs['itemValue'])

        dataDict = {
            "areaScale": areaScale,  # 専有面積
            "item1": itemList[0],  # 設備
            "item2": itemList[1],
            "item3": itemList[2],
            "item4": itemList[3],
        }

        return dataDict

# ----------------------------------------------------------------------------------


    def _thirdPageInfo(self, **kwargs):
        itemList = self._textCleaner(by=kwargs['itemBy'], value=kwargs['itemValue'])
        chatGpt1 = "ここに関数をいれる"

        dataDict = {
            "item5": itemList[4],  # 設備
            "item6": itemList[5],
            "item7": itemList[6],
            "item8": itemList[7],
            "chatGpt1": chatGpt1,
        }

        return dataDict


# ----------------------------------------------------------------------------------


    def _fourthPageInfo(self, **kwargs):
        itemList = self._textCleaner(by=kwargs['itemBy'], value=kwargs['itemValue'])
        chatGpt1 = "ここに関数をいれる"

        dataDict = {
            "item5": itemList[4],  # 設備
            "item6": itemList[5],
            "item7": itemList[6],
            "item8": itemList[7],
            "chatGpt1": chatGpt1,
        }

        return dataDict


# ----------------------------------------------------------------------------------