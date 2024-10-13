# coding: utf-8
# $$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$

# $$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$
# import
import time
from selenium.webdriver.chrome.webdriver import WebDriver
from datetime import datetime
from typing import Dict, Any, List, Tuple

from selenium.webdriver.remote.webelement import WebElement


# 自作モジュール
from .utils import Logger
from .elementManager import ElementManager
from .AiOrder import ChatGPTOrder
from .textManager import TextManager
from ..dataclass import ListPageInfo, DetailPageInfo
from .SQLite import SQLite
from .decorators import Decorators

decoInstance = Decorators(debugMode=True)


# $$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$
# **********************************************************************************


class TextDataInSQLite:
    def __init__(self, chrome: WebDriver, debugMode=True):
        # logger
        self.getLogger = Logger(__name__, debugMode=debugMode)
        self.logger = self.getLogger.getLogger()

        self.chrome = chrome
        self.currentDate = datetime.now().strftime('%y%m%d_%H%M%S')
        self.element = ElementManager(chrome=self.chrome, debugMode=debugMode)
        self.chatGPT = ChatGPTOrder(debugMode=debugMode)
        self.textManager = TextManager(debugMode=debugMode)
        self.SQLite = SQLite(debugMode=debugMode)


# ----------------------------------------------------------------------------------
# nameを主としたサブ辞書の作成

    @decoInstance.funcBase
    def flowMoveGetElement(self, tableValue: int, tableName: str ,delay: int = 2):
        # 一覧ページで取得
        listPageInfo = self._listPageInfo(tableValue=tableValue)

        # 移動
        self.element.clickElement(
            by='xpath',
            value=f"//div[@class='searchResultLsit'][{tableValue}]//tr[@class='resultLsitBtnTr2']//a[contains(text(), '物件画像')]"
        )

        time.sleep(delay)

        # 詳細ページで取得
        detailPageInfo = self._detailPageInfo()

        # 辞書の結合
        mergeDict = {**listPageInfo, **detailPageInfo}

        # SQLiteに書込
        self.SQLite.insertDictData(tableName=tableName, inputDict=mergeDict)

        return mergeDict


# ----------------------------------------------------------------------------------
# # 一覧ページから取得

    @decoInstance.funcBase
    def _listPageInfo(self, tableValue: int) -> Dict[str, WebElement]:
        listInstance = self._listPageInfo(tableValue)
        return self._getListPageElement(listPageInfo=listInstance)


# ----------------------------------------------------------------------------------
# 詳細ページからデータを取得

    @decoInstance.funcBase
    def _detailPageInfo(self) -> Dict[str, WebElement]:
        detailInstance = self._detailPageInfo()
        return self._getDetailPageElement(detailPageInfo=detailInstance)


# ----------------------------------------------------------------------------------


    def _listPageInfo(self, tableValue: int):
        return ListPageInfo(
            stationBy="xpath",
            stationValue=f"//div[@class='searchResultLsit'][{tableValue}]//tr[@class='searchResultLsitTabTr1']//div[@class='vicinityInfo']/p[@class='new']/span[1]",
            trainLineBy="xpath",
            trainLineValue=f"//div[@class='searchResultLsit'][{tableValue}]//tr[@class='searchResultLsitTabTr1']//div[@class='vicinityInfo']/p[@class='new']/span[2]",
            walkingBy="xpath",
            walkingValue=f"//div[@class='searchResultLsit'][{tableValue}]//tr[@class='searchResultLsitTabTr1']//div[@class='vicinityInfo']/p[@class='new']/span[3]",
        )


# ----------------------------------------------------------------------------------


    def _detailPageInfo(self):
        return DetailPageInfo(
            nameBy="xpath",
            nameValue=f"//th[text()='物件名']/following-sibling::td[1]/span",
            adBy="xpath",
            adValue="//th[text()='広告可否']/following-sibling::td[1]/span",
            areaBy="xpath",
            areaValue="//th[text()='専有面積']/following-sibling::td[1]/span",
            itemBy="xpath",
            itemValue="//th[text()='広告可否']/following-sibling::td[1]/span",
            addressBy="xpath",
            addressValue="//th[text()='物件所在地']/following-sibling::td[1]/span",
            rentBy="xpath",
            rentValue="//th[text()='賃料']/following-sibling::td[1]/span",
            managementCostBy="xpath",
            managementCostValue="//th[text()='管理費等']/following-sibling::td[1]/span",
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
