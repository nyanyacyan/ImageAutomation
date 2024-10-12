# coding: utf-8
# $$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$

# $$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$
# import
from selenium.webdriver.chrome.webdriver import WebDriver
from datetime import datetime
from typing import Dict, Any, List, Tuple
from dataclasses import dataclass


# 自作モジュール
from .utils import Logger
from .elementManager import ElementManager
from .AiOrder import ChatGPTOrder
from .textManager import TextManager


# $$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$
# **********************************************************************************

@dataclass
class MetaInfo:
    textBy: str
    textValue: str
    titleBy: str
    titleValue: str
    placementPage: str
    priority: str
    status: str

# ここから先のものを追記する→
# 引数の整理する→引数を返す関数を作成する
# mergeDictを整理する

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


    def mergeDict(
        self,
        name: str,
        textBy: str, textValue: str,
        titleBy: str, titleValue: str,
        placementPage: str, priority: str, status: str,
        trainLineBy: str, trainLineValue: str,
        stationBy: str, stationValue: str,
        addressBy: str, addressValue: str,
        walkingBy: str, walkingValue: str,
        areaBy: str, areaValue: str,
        itemBy: str, itemValue: str,
        firstWord: str, lastWord: str, ifValueList: List,
        rentBy: str, rentValue: str,
        managementCostBy: str, managementCostValue: str,
        prompt1: str,
        fixedPrompt :str,
        endpointUrl: str,
        model: str,
        apiKey: str,
        maxTokens: int,
        maxlen: int,
        prompt2: str,
    ):

        metaInfo = self._metaInfo(
            textBy=textBy, textValue=textValue,
            titleBy=titleBy, titleValue=titleValue,
            placementPage=placementPage, priority=priority, status=status
        )

        topPageInfo = self._topPageInfo(
            trainLineBy=trainLineBy, trainLineValue=trainLineValue,
            stationBy=stationBy, stationValue=stationValue,
            addressBy=addressBy, addressValue=addressValue,
            walkingBy=walkingBy, walkingValue=walkingValue,
        )

        secondPageInfo = self._secondPageInfo(
            areaBy=areaBy, areaValue=areaValue,
            itemBy=itemBy, itemValue=itemValue,
            firstWord=firstWord, lastWord=lastWord, ifValueList=ifValueList,
            trainLineBy=trainLineBy, trainLineValue=trainLineValue,
            stationBy=stationBy, stationValue=stationValue,
            walkingBy=walkingBy, walkingValue=walkingValue,
            addressBy=addressBy, addressValue=addressValue,
            rentBy=rentBy, rentValue=rentValue,
            managementCostBy=managementCostBy, managementCostValue=managementCostValue,
        )

        thirdPageInfo = self._thirdPageInfo(
            itemBy=itemBy, itemValue=itemValue,
            prompt1=prompt1,
            fixedPrompt=fixedPrompt,
            endpointUrl=endpointUrl,
            model=model,
            apiKey=apiKey,
            maxTokens=maxTokens,
            maxlen=maxlen
        )

        fourthPageInfo = self._fourthPageInfo(
            itemBy=itemBy, itemValue=itemValue,
            prompt2=prompt2,
            fixedPrompt=fixedPrompt,
            endpointUrl=endpointUrl,
            model=model,
            apiKey=apiKey,
            maxTokens=maxTokens,
            maxlen=maxlen
        )

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

    def _metaInfo(
        self,
        textBy: str, textValue: str,
        titleBy: str, titleValue: str,
        placementPage: str, priority: str, status: str
    ):

        date = self.currentDate
        getText = self.getElement(by=textBy, value=textValue)
        url = self.chrome.current_url()
        title = self.getElement(by=titleBy, value=titleValue)

        dataDict = {
            "getText": getText,
            "createTime": date,
            "url": url,  # URL
            "title": title,  # サイトタイトル
            "placementPage": placementPage,
            "priority": priority,
            "status": status,
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


    def _secondPageInfo(
        self,
        areaBy: str, areaValue: str,
        itemBy: str, itemValue: str,
        firstWord: str, lastWord: str, ifValueList: List,
        trainLineBy: str, trainLineValue: str,
        stationBy: str, stationValue: str,
        walkingBy: str, walkingValue: str,
        addressBy: str, addressValue: str,
        rentBy: str, rentValue: str,
        managementCostBy: str, managementCostValue: str
    ):

        areaScale = self.element.getElement(by=areaBy, value=areaValue)
        itemList = self.element._textCleaner(by=itemBy, value=itemValue)

        # 要素の取得を行ってリスト化
        commentElementLst = self._textJoinList(
            ifValueList=ifValueList,
            trainLineBy=trainLineBy, trainLineValue=trainLineValue,
            stationBy=stationBy, stationValue=stationValue,
            walkingBy=walkingBy, walkingValue=walkingValue,
            addressBy=addressBy, addressValue=addressValue,
            rentBy=rentBy, rentValue=rentValue,
            managementCostBy=managementCostBy, managementCostValue=managementCostValue
        )
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
        fixedPrompt :str,
        endpointUrl: str,
        model: str,
        apiKey: str,
        maxTokens: int,
        maxlen: int
    ):

        itemList = self._textCleaner(by=itemBy, value=itemValue)
        chatGpt1 = self.chatGPT.resultOutput(
            prompt=prompt1,
            fixedPrompt=fixedPrompt,
            endpointUrl=endpointUrl,
            model=model,
            apiKey=apiKey,
            maxlen=maxlen,
            maxTokens=maxTokens,
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
        itemBy: str, itemValue: str,
        prompt2: str,
        fixedPrompt :str,
        endpointUrl: str,
        model: str,
        apiKey: str,
        maxTokens: int,
        maxlen: int
    ):

        itemList = self._textCleaner(by=itemBy, value=itemValue)
        chatGpt1 = self.chatGPT.resultOutput(
            prompt=prompt2,
            fixedPrompt=fixedPrompt,
            endpointUrl=endpointUrl,
            model=model,
            apiKey=apiKey,
            maxlen=maxlen,
            maxTokens=maxTokens,
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