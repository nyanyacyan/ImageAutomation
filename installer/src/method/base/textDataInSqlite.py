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
from ..dataclass import MetaInfo, TopPageInfo, SecondPageInfo, ThirdFourthInfo


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

    def _metaInfo(self, metaInfo:MetaInfo):

        date = self.currentDate
        getText = self.getElement(by=metaInfo.textBy, value=metaInfo.textValue)
        url = self.chrome.current_url()
        title = self.getElement(by=metaInfo.titleBy, value=metaInfo.titleValue)

        dataDict = {
            "getText": getText,
            "createTime": date,
            "url": url,  # URL
            "title": title,  # サイトタイトル
            "placementPage": metaInfo.placementPage,
            "priority": metaInfo.priority,
            "status": metaInfo.status,
        }

        return dataDict


# ----------------------------------------------------------------------------------


    def _topPageInfo(self, topPageInfo: TopPageInfo):

        trainLine = self.element.getElement(by=topPageInfo.trainLineBy, value=topPageInfo.trainLineValue)
        station = self.element.getElement(by=topPageInfo.stationBy, value=topPageInfo.stationValue)
        walking = self.element.getElement(by=topPageInfo.walkingBy, value=topPageInfo.walkingValue)
        address = self.element._getAddress(by=topPageInfo.addressBy, value=topPageInfo.addressValue)

        dataDict = {
            "trainLine": trainLine,  # 路線名
            "station": station,  # 駅名
            "walking": walking,  # 徒歩
            "address": address,  # 都道府県
        }

        return dataDict


# ----------------------------------------------------------------------------------


    def _secondPageInfo(self, secondPageInfo: SecondPageInfo):

        areaScale = self.element.getElement(by=secondPageInfo.areaBy, value=secondPageInfo.areaValue)
        itemList = self.element._textCleaner(by=secondPageInfo.itemBy, value=secondPageInfo.itemValue)

        # 要素の取得を行ってリスト化
        commentElementLst = self._textJoinList(
            ifValueList=secondPageInfo.ifValueList,
            trainLineBy=secondPageInfo.trainLineBy, trainLineValue=secondPageInfo.trainLineValue,
            stationBy=secondPageInfo.stationBy, stationValue=secondPageInfo.stationValue,
            walkingBy=secondPageInfo.walkingBy, walkingValue=secondPageInfo.walkingValue,
            addressBy=secondPageInfo.addressBy, addressValue=secondPageInfo.addressValue,
            rentBy=secondPageInfo.rentBy, rentValue=secondPageInfo.rentValue,
            managementCostBy=secondPageInfo.managementCostBy, managementCostValue=secondPageInfo.managementCostValue
        )
        # 最初と最後に文言を追加
        commentElementLst = self.textManager.addListFirstLast(lst=commentElementLst, firstWord=secondPageInfo.firstWord, lastWord=secondPageInfo.lastWord)
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


    def _textJoinList(self, secondPageInfo: SecondPageInfo):

        conditions = [
            (secondPageInfo.trainLineBy, secondPageInfo.trainLineValue),
            (secondPageInfo.stationBy, secondPageInfo.stationValue),
            (secondPageInfo.walkingBy, secondPageInfo.walkingValue),
            (secondPageInfo.addressBy, secondPageInfo.addressValue),
            (secondPageInfo.rentBy, secondPageInfo.rentValue),
            (secondPageInfo.managementCostBy, secondPageInfo.managementCostValue)
        ]

        return self.element._getElementList(conditions=conditions, ifValueList=secondPageInfo.ifValueList)


# ----------------------------------------------------------------------------------


    def _thirdPageInfo(self, thirdFourthInfo: ThirdFourthInfo):
        itemList = self._textCleaner(by=thirdFourthInfo.itemBy, value=thirdFourthInfo.itemValue)
        chatGpt1 = self.chatGPT.resultOutput(
            prompt=thirdFourthInfo.prompt,
            fixedPrompt=thirdFourthInfo.fixedPrompt,
            endpointUrl=thirdFourthInfo.endpointUrl,
            model=thirdFourthInfo.model,
            apiKey=thirdFourthInfo.apiKey,
            maxlen=thirdFourthInfo.maxlen,
            maxTokens=thirdFourthInfo.maxTokens,
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


    def _fourthPageInfo(self, thirdFourthInfo: ThirdFourthInfo):

        itemList = self._textCleaner(by=thirdFourthInfo.itemBy, value=thirdFourthInfo.itemValue)
        chatGpt2 = self.chatGPT.resultOutput(
            prompt=thirdFourthInfo.prompt,
            fixedPrompt=thirdFourthInfo.fixedPrompt,
            endpointUrl=thirdFourthInfo.endpointUrl,
            model=thirdFourthInfo.model,
            apiKey=thirdFourthInfo.apiKey,
            maxlen=thirdFourthInfo.maxlen,
            maxTokens=thirdFourthInfo.maxTokens,
        )

        dataDict = {
            "item5": itemList[4],  # 設備
            "item6": itemList[5],
            "item7": itemList[6],
            "item8": itemList[7],
            "chatGpt2": chatGpt2,
        }

        return dataDict


# ----------------------------------------------------------------------------------