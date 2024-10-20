# coding: utf-8
# $$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$

# $$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$
# import
import time, os
from selenium.webdriver.chrome.webdriver import WebDriver
from datetime import datetime
from typing import Dict, Any, List, Tuple
from dotenv import load_dotenv

from selenium.webdriver.remote.webelement import WebElement


# 自作モジュール
from .utils import Logger
from .elementManager import ElementManager
from .AiOrder import ChatGPTOrder
from .textManager import TextManager
from ..dataclass import ListPageInfo, DetailPageInfo
from .SQLite import SQLite
from .decorators import Decorators
from .jumpTargetPage import JumpTargetPage
from ..const import ChatGptPrompt, ChatgptUtils
from ..constElementPath import ElementPath, ElementSpecify
from ..constSqliteTable import TableName

decoInstance = Decorators(debugMode=True)

load_dotenv()

# $$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$
# **********************************************************************************


class TextDataInSQLite:
    def __init__(self, chrome: WebDriver, debugMode=True):
        # logger
        self.getLogger = Logger(__name__, debugMode=debugMode)
        self.logger = self.getLogger.getLogger()

        self.chrome = chrome
        self.textTableName = TableName.TEXT_TABLE_COLUMNS
        self.currentDate = datetime.now().strftime('%y%m%d_%H%M%S')
        self.element = ElementManager(chrome=self.chrome, debugMode=debugMode)
        self.chatGPT = ChatGPTOrder(debugMode=debugMode)
        self.textManager = TextManager(debugMode=debugMode)
        self.SQLite = SQLite(debugMode=debugMode)
        self.jumpTargetPage = JumpTargetPage(chrome=self.chrome, debugMode=debugMode)


# ----------------------------------------------------------------------------------
# nameを主としたサブ辞書の作成

    @decoInstance.funcBase
    def flowMoveGetElement(self, targetUrl: str ,retryCount: int = 5, delay: int = 2):

        allList = []
        for i in range(retryCount):
            # ジャンプしてURLへ移動
            self.jumpTargetPage.flowJumpTargetPage(targetUrl=targetUrl)
            time.sleep(delay)

            # 一度更新
            self.chrome.refresh()
            time.sleep(delay)

            # 検索画面を消去
            self.element.clickElement(
                by=ElementSpecify.XPATH.value,
                value=ElementPath.SEARCH_DELETE_BTN_PATH.value
            )
            time.sleep(delay)
            metaInfo = self._metaInfo()

            # 一覧ページにて要素を取得
            listPageInfo = self._listPageInfo(tableValue={i + 1})

            # 詳細ページへ移動
            self.element.clickElement(
                by=ElementSpecify.XPATH.value,
                value=ElementPath.DETAIL_PAGE_BTN_PATH.value.format(i + 1)
            )
            time.sleep(delay)

            # 詳細ページでtextを取得
            detailPageInfo = self._detailPageInfo()

            # 辞書の結合
            mergeDict = {**metaInfo, **listPageInfo, **detailPageInfo}

            # SQLiteに書込
            id = self.SQLite.insertDictData(tableName=self.textTableName, inputDict=mergeDict)
            time.sleep(delay)

            secondComment = self.createSecondPageComment(mergeDict=mergeDict)

            # TODO 取得したtextから整理、手直しをする
            thirdComment = self.chatGPTComment(
                mergeDict=mergeDict,
                startValue=5,
                endValue=8,
                maxlen=30
            )

            fourthPrompt = self.chatGPTComment(
                mergeDict=mergeDict,
                startValue=9,
                endValue=12,
                maxlen=30
            )

            updateColumnsData = {
                "secondComment": secondComment,
                "thirdComment": thirdComment,
                "fourthPrompt": fourthPrompt
            }

            mergeDict = {**metaInfo, **listPageInfo, **detailPageInfo, **updateColumnsData}
            allList.append(mergeDict)


            # SQLiteに書込
            self.SQLite.updateData(
                tableName=self.textTableName,
                updateColumnsData=updateColumnsData,
                rowId=id
            )
            time.sleep(delay)


        return allList


# ----------------------------------------------------------------------------------
# 3ページ目のChatGPT

    async def chatGPTComment(self, mergeDict: Dict, itemStartValue: int, itemEndValue: int, maxlen: int):
        prompt = self.ChatGPTPromptCreate(mergeDict=mergeDict, itemStartValue=itemStartValue, itemEndValue=itemEndValue, maxlen=maxlen)
        await self.chatGPT.resultOutput(
            prompt=prompt,
            fixedPrompt=ChatGptPrompt.fixedPrompt.value,
            endpointUrl=ChatgptUtils.endpointUrl.value,
            model=ChatgptUtils.model.value,
            apiKey=os.getenv('CHATGPT_APIKEY'),
            maxlen=maxlen,
            maxTokens=ChatgptUtils.MaxToken.value
        )


# ----------------------------------------------------------------------------------
# Prompt生成
# 文字数制限はここで入力

    def ChatGPTPromptCreate(self, mergeDict: Dict, itemStartValue: int, itemEndValue: int, maxlen: int):
        items = [mergeDict['item'][i] for i in range(itemStartValue, itemEndValue + 1)]
        prompt = ChatGptPrompt.recommend.value.format(
            maxlen=maxlen,
            item0=items[0],
            item1=items[1],
            item2=items[2],
            item3=items[3],
        )

        return prompt


# ----------------------------------------------------------------------------------
# 2ページ目のコメント作成

    def createSecondPageComment(self, mergeDict: str):
        # 2枚目コメント→つなぎ合わせたもの
        result = self.SQLite.getSortColOneData(
            tableName = self.tableName,
            primaryKeyCol = "name",
            primaryKeyColValue = mergeDict.get('name'),
            cols=['trainLine', 'station', 'walking', 'rent', 'managementCost']
        )

        trainLine = result.get('trainLine', '-')
        station = result.get('station', '-')
        walking = result.get('walking', '-')
        rent = result.get('rent', '-')
        managementCost = result.get('managementCost', '-')

        commentParts = [
            "今回は",
            f"{trainLine} の {station}駅 から {walking} の物件です。",
            f"賃料は {rent}",
            f"管理費等は {managementCost}",
            "紹介するよ"
        ]

        secondComment = '\n'.join(commentParts)
        return {'secondComment': secondComment}


# ----------------------------------------------------------------------------------
# # 一覧ページから取得

    @decoInstance.funcBase
    def _listPageInfo(self, tableValue: int) -> Dict[str, WebElement]:
        listInstance = self._listPageInfoValue(tableValue)
        return self._getListPageElement(listPageInfo=listInstance)


# ----------------------------------------------------------------------------------
# 詳細ページからデータを取得

    @decoInstance.funcBase
    def _detailPageInfo(self) -> Dict[str, WebElement]:
        detailInstance = self._detailPageInfoValue()
        return self._getDetailPageElement(detailPageInfo=detailInstance)


# ----------------------------------------------------------------------------------


    def _metaInfo(self):
        currentUrl = self.chrome.current_url
        currentDate = self.currentDate

        dataDict = {
            "url": currentUrl,
            "createTime": currentDate
        }
        return dataDict


# ----------------------------------------------------------------------------------


    def _listPageInfoValue(self, tableValue: int):
        return ListPageInfo(
            stationBy=ElementSpecify.XPATH.value,
            stationValue=ElementPath.STATION_VALUE.value.format(tableValue),
            trainLineBy=ElementSpecify.XPATH.value,
            trainLineValue=ElementPath.TRAIN_LINE.value.format(tableValue),
            walkingBy=ElementSpecify.XPATH.value,
            walkingValue=ElementPath.WAKING.value.format(tableValue),
        )


# ----------------------------------------------------------------------------------


    def _detailPageInfoValue(self):
        return DetailPageInfo(
            nameBy=ElementSpecify.XPATH.value,
            nameValue=ElementPath.NAME.value,
            adBy=ElementSpecify.XPATH.value,
            adValue=ElementPath.AD.value,
            areaBy=ElementSpecify.XPATH.value,
            areaValue=ElementPath.AREA.value,
            itemBy=ElementSpecify.XPATH.value,
            itemValue=ElementPath.ITEM.value,
            addressBy=ElementSpecify.XPATH.value,
            addressValue=ElementPath.ADDRESS.value,
            rentBy=ElementSpecify.XPATH.value,
            rentValue=ElementPath.RENT.value,
            managementCostBy=ElementSpecify.XPATH.value,
            managementCostValue=ElementPath.MANAGEMENT_COST.value,
        )


# ----------------------------------------------------------------------------------


    @decoInstance.funcBase
    def _getListPageElement(self, listPageInfo: ListPageInfo):
        trainLine = self.element.getElement(by=listPageInfo.trainLineBy, value=listPageInfo.trainLineValue)
        station = self.element.getElement(by=listPageInfo.stationBy, value=listPageInfo.stationValue)
        walking = self.element.getElement(by=listPageInfo.walkingBy, value=listPageInfo.walkingValue)

        dataDict = {
            "trainLine": trainLine,  # 路線名
            "station": station,  # 駅名
            "walking": walking,  # 徒歩
        }

        return dataDict


# ----------------------------------------------------------------------------------


    @decoInstance.funcBase
    def _getDetailPageElement(self, detailPageInfo: DetailPageInfo):
        name = self.element.getElement(by=detailPageInfo.trainLineBy, value=detailPageInfo.trainLineValue)
        ad = self.element.getElement(by=detailPageInfo.adBy, value=detailPageInfo.adValue)
        area = self.element.getElement(by=detailPageInfo.areaBy, value=detailPageInfo.areaValue)
        item = self.element.getElement(by=detailPageInfo.itemBy, value=detailPageInfo.itemValue)
        address = self.element.getElement(by=detailPageInfo.addressBy, value=detailPageInfo.addressValue)
        rent = self.element.getElement(by=detailPageInfo.rentBy, value=detailPageInfo.rentValue)
        managementCost = self.element.getElement(by=detailPageInfo.managementCostBy, value=detailPageInfo.managementCostValue)

        dataDict = {
            "name": name,  # 物件名
            "ad": ad,  # 広告可否
            "area": area,  # 路線名
            "item": item,  # 駅名
            "address": address,  # 徒歩
            "rent": rent,  # 徒歩
            "managementCost": managementCost,  # 徒歩
        }

        return dataDict


# ----------------------------------------------------------------------------------
