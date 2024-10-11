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
        self.dictManager = ElementManager(debugMode=debugMode)


# ----------------------------------------------------------------------------------


    def mergeDict(self, name: str):
        metaInfo = self._topPageInfo()
        topPageInfo = self._secondPageInfo()
        secondPageInfo = self._secondPageInfo()
        thirdPageInfo = self._thirdPageInfo()
        fourthPageInfo = self._fourthPageInfo()

        # サブ辞書の初期化
        dataDict = self.dictManager._initDict(name=name)

        # 順番にサブ辞書を追加していく
        dataDictInMeta = self.dictManager.updateSubDict(dictBox=dataDict, name=name, inputDict=metaInfo)
        dataDictInTop = self.dictManager.updateSubDict(dictBox=dataDictInMeta, name=name, inputDict=topPageInfo)
        dataDictInSecond = self.dictManager.updateSubDict(dictBox=dataDictInTop, name=name, inputDict=secondPageInfo)
        dataDictInThird = self.dictManager.updateSubDict(dictBox=dataDictInSecond, name=name, inputDict=thirdPageInfo)
        result = self.dictManager.updateSubDict(dictBox=dataDictInThird, name=name, inputDict=fourthPageInfo)

        return result


# ----------------------------------------------------------------------------------
# metaInfo

    def _metaInfo(self):
        pass


# ----------------------------------------------------------------------------------


    def _topPageInfo(self):
        pass


# ----------------------------------------------------------------------------------


    def _secondPageInfo(self):
        pass


# ----------------------------------------------------------------------------------


    def _thirdPageInfo(self):
        pass


# ----------------------------------------------------------------------------------


    def _fourthPageInfo(self):
        pass


# ----------------------------------------------------------------------------------