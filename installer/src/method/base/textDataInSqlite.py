# coding: utf-8
# $$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$

# $$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$
# import
from selenium.webdriver.chrome.webdriver import WebDriver
from datetime import datetime
from typing import Dict, Any, List, Tuple



# 自作モジュール
from .utils import Logger
from .elementManager import ElementManager
from .AiOrder import ChatGPTOrder
from .textManager import TextManager


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
        self.chatGPT = ChatGPTOrder(debugMode=debugMode)
        self.textManager = TextManager(debugMode=debugMode)


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
        date = self.currentDate
        getText = self.getElement(by=kwargs['textBy'], value=kwargs['textValue'])
        url = self.chrome.current_url()
        title = self.getElement(by=kwargs['titleBy'], value=kwargs['titleValue'])

        dataDict = {
            "getText": getText,
            "createTime": date,
            "url": url,  # URL
            "title": title,  # サイトタイトル
            "placementPage": kwargs['placementPage'],
            "priority": kwargs['priority'],
            "status": kwargs['status'],
        }

        return dataDict


# ----------------------------------------------------------------------------------


    def _topPageInfo(
        self,
        trainLineBy: str, trainLineValue: str,
        stationBy: str, stationValue: str,
        addressBy: str, addressValue: str,
        walkingBy: str, walkingValue: str
    ):

        trainLine = self.element.getElement(by=trainLineBy, value=trainLineValue)
        station = self.element.getElement(by=stationBy, value=stationValue)
        walking = self.element.getElement(by=walkingBy, value=walkingValue)
        address = self.element._getAddress(by=addressBy, value=addressValue)

        dataDict = {
            "trainLine": trainLine,  # 路線名
            "station": station,  # 駅名
            "walking": walking,  # 徒歩
            "address": address,  # 都道府県
        }

        return dataDict


# ----------------------------------------------------------------------------------


    def _secondPageInfo(self, areaBy: str, areaValue: str, itemBy: str, itemValue: str, firstWord: str, lastWord: str):
        areaScale = self.element.getElement(by=areaBy, value=areaValue)
        itemList = self.element._textCleaner(by=itemBy, value=itemValue)

        # 要素の取得を行ってリスト化
        commentElementLst = self._textJoinList()
        # 最初と最後に文言を追加
        commentElementLst = self.textManager.addListFirstLast(lst=commentElementLst, firstWord=firstWord, lastWord=lastWord)
        # 全てを繋げてコメントに変換
        comment = self.textManager.textJoin(joinWordsList=commentElementLst)

        dataDict = {
            "areaScale": areaScale,  # 専有面積
            "item1": itemList[0],  # 設備
            "item2": itemList[1],
            "item3": itemList[2],
            "item4": itemList[3],
            "comment": comment
        }

        return dataDict

# ----------------------------------------------------------------------------------


    def _textJoinList(
        self,
        ifValueList: List,
        trainLineBy: str, trainLineValue: str,
        stationBy: str, stationValue: str,
        walkingBy: str, walkingValue: str,
        addressBy: str, addressValue: str,
        rentBy: str, rentValue: str,
        managementCostBy: str, managementCostValue: str
    ):

        conditions = [
            (trainLineBy, trainLineValue),
            (stationBy, stationValue),
            (walkingBy, walkingValue),
            (addressBy, addressValue),
            (rentBy, rentValue),
            (managementCostBy, managementCostValue)
        ]

        return self.element._getElementList(conditions=conditions, ifValueList=ifValueList)


# ----------------------------------------------------------------------------------


    def _thirdPageInfo(
        self,
        itemBy: str, itemValue: str,
        prompt1: str,
        fixedPrompt1 :str,
        endpointUrl1: str,
        model1: str,
        apiKey1: str,
        maxTokens1: int,
        maxlen1: int
    ):

        itemList = self._textCleaner(by=itemBy, value=itemValue)
        chatGpt1 = self.chatGPT.resultOutput(
            prompt=prompt1,
            fixedPrompt=fixedPrompt1,
            endpointUrl=endpointUrl1,
            model=model1,
            apiKey=apiKey1,
            maxlen=maxlen1,
            maxTokens=maxTokens1,
        )

        dataDict = {
            "item5": itemList[4],  # 設備
            "item6": itemList[5],
            "item7": itemList[6],
            "item8": itemList[7],
            "chatGpt1": chatGpt1,
        }

        return dataDict


# ----------------------------------------------------------------------------------


    def _fourthPageInfo(
        self,
        itemBy: str,
        itemValue: str,
        prompt2: str,
        fixedPrompt2: str,
        endpointUrl2: str,
        model2: str,
        apiKey2: str,
        maxTokens2: int,
        maxlen2: int
    ):

        itemList = self._textCleaner(by=itemBy, value=itemValue)
        chatGpt1 = self.chatGPT.resultOutput(
            prompt=prompt2,
            fixedPrompt=fixedPrompt2,
            endpointUrl=endpointUrl2,
            model=model2,
            apiKey=apiKey2,
            maxlen=maxlen2,
            maxTokens=maxTokens2,
        )

        dataDict = {
            "item5": itemList[4],  # 設備
            "item6": itemList[5],
            "item7": itemList[6],
            "item8": itemList[7],
            "chatGpt1": chatGpt1,
        }

        return dataDict


# ----------------------------------------------------------------------------------