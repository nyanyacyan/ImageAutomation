# coding: utf-8
# $$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$

# $$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$
# import
import time
from selenium.webdriver.chrome.webdriver import WebDriver
from datetime import datetime
from typing import Dict, Any

# 自作モジュール
from .utils import Logger
from ..const import NGWordList, Address
from .decorators import Decorators
from .textManager import TextManager


decoInstance = Decorators(debugMode=True)


# $$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$
# **********************************************************************************


class ElementManager:
    def __init__(self, chrome: WebDriver, debugMode=True):
        # logger
        self.getLogger = Logger(__name__, debugMode=debugMode)
        self.logger = self.getLogger.getLogger()

        self.chrome = chrome
        self.currentDate = datetime.now().strftime('%y%m%d_%H%M%S')
        self.textManager = TextManager(debugMode=debugMode)


# ----------------------------------------------------------------------------------


    def getElement(self, by, value):
        if by == "id":
            return self.chrome.find_element_by_id(value)
        elif by == "css":
            return self.chrome.find_element_by_css_selector(value)
        elif by == "xpath":
            return self.chrome.find_element_by_xpath(value)
        elif by == "tag":
            return self.chrome.find_element_by_tag_name(value)
        elif by == "link":
            return self.chrome.find_element_by_link_text(value)
        elif by == "name":
            return self.chrome.find_element_by_name(value)
        elif by == "class":
            return self.chrome.find_element_by_class_name(value)
        else:
            raise ValueError("定義してるもの以外のものを指定してます")


# ----------------------------------------------------------------------------------
# 複数

    def getElements(self, by: str, value: str):
        if by == "id":
            return self.chrome.find_elements_by_id(value)
        elif by == "css":
            return self.chrome.find_elements_by_css_selector(value)
        elif by == "xpath":
            return self.chrome.find_elements_by_xpath(value)
        elif by == "tag":
            return self.chrome.find_elements_by_tag_name(value)
        elif by == "link":
            return self.chrome.find_elements_by_link_text(value)
        elif by == "name":
            return self.chrome.find_elements_by_name(value)
        elif by == "class":
            return self.chrome.find_elements_by_class_name(value)
        else:
            raise ValueError("定義してるもの以外のものを指定してます")


# ----------------------------------------------------------------------------------


    @decoInstance.funcBase
    def clickClearInput(self, by: str, value: str, inputText: str, delay: int = 2):
        element = self.getElement(by=by, value=value)
        element.click()
        time.sleep(delay)
        element.clear()
        time.sleep(delay)
        element.send_keys(inputText)


# ----------------------------------------------------------------------------------


    def clickElement(self, by: str, value: str):
        element = self.getElement(by=by, value=value)
        element.click()
        return


# ----------------------------------------------------------------------------------


    @decoInstance.funcBase
    def getText(self, by: str, value: str):
        element = self.getElement(by=by, value=value)
        return element.text


# ----------------------------------------------------------------------------------


    @decoInstance.funcBase
    def getImageUrl(self, by: str, value: str):
        element = self.getElement(by=by, value=value)
        return element.get_attribute("src")


# ----------------------------------------------------------------------------------


    def _getItemsList(self, by: str, value: str):
        itemElements = self.getElement(by=by, value=value)
        itemsText = itemElements.text
        itemsList = itemsText.split('，')
        return itemsList


# ----------------------------------------------------------------------------------


    def _textCleaner(self, by: str, value: str):
        targetList = self._getItemsList(by=by, value=value)
        ngWords = NGWordList.ngWords.value
        filterWordsList = self.textManager.filterWords(targetList=targetList, ngWords=ngWords)
        return filterWordsList


# ----------------------------------------------------------------------------------


    def _getAddress(self, by: str, value: str):
        fullAddress = self.getElement(by=by, value=value)
        addressList = Address.addressList.value

        for address in addressList:
            if fullAddress.startswith(address):
                return address


# ----------------------------------------------------------------------------------
# 辞書dataの初期化

    def _initDict(self, name: str):# -> dict[str, dict]:
        return {name: {}}


# ----------------------------------------------------------------------------------
# サブ辞書の中身を入れ込む

    def updateSubDict(self, dictBox: dict[str, dict[str, Any]], name: str, inputDict: Dict[str, Any]):
        dictBox[name].update(inputDict)
        return dictBox


# ----------------------------------------------------------------------------------


    def getTextAndMeta(
        self,
        name: str,

        # 1枚目
        trainLineBy: str,
        trainLineValue: str,
        stationBy: str,
        stationValue: str,
        walkingBy: str,
        walkingValue: str,
        addressBy: str,
        addressValue: str,

        # 2枚目以降
        itemBy: str,
        itemValue: str,
        by: str,
        value: str,
        titleBy: str,
        titleValue: str,
        areaBy: str,
        areaValue: str,
        placementPage: int,
        priority: int,
        chatGpt1: str,
        chatGpt2: str
    ):

        dataDict = {}
        name = name
        date = self.currentDate
        getText = self.getElement(by=by, value=value)
        url = self.chrome.current_url()
        title = self.getElement(by=titleBy, value=titleValue)

        # 1枚目
        trainLine = self._getAddress(by=trainLineBy, value=trainLineValue)
        station = self._getAddress(by=stationBy, value=stationValue)
        address = self._getAddress(by=addressBy, value=addressValue)
        walking = self._getAddress(by=walkingBy, value=walkingValue)


        areaScale = self.getElement(by=areaBy, value=areaValue)
        itemList = self._textCleaner(by=itemBy, value=itemValue)
        chatGpt1 = "ここに関数をいれる"
        chatGpt1 = "ここに関数をいれる"

        if getText:
            status = "success"
        else:
            status = "failure"

        dataDict[name]={
            # meta
            "name": name,
            "getText": getText,
            "createTime": date,
            "url": url,  # URL
            "title": title,  # サイトタイトル
            "placementPage": placementPage,
            "priority": priority,
            "status": status,

            # 1枚目
            "trainLine": trainLine,
            "station": station,  # 駅名
            "address": address,  # 都道府県
            "walking": walking,  # 徒歩

            # 2枚目
            "areaScale": areaScale,  # 専有面積
            "item1": itemList[0],  # 設備
            "item2": itemList[1],
            "item3": itemList[2],
            "item4": itemList[3],

            # 3枚目
            "item5": itemList[4],  # 設備
            "item6": itemList[5],
            "item7": itemList[6],
            "item8": itemList[7],
            "chatGpt1": chatGpt1,


            # 4枚目
            "item9": itemList[8],  # 設備
            "item10": itemList[9],
            "item11": itemList[10],
            "item12": itemList[11],
            "chatGpt2": chatGpt2,
        }

        return dataDict


# ----------------------------------------------------------------------------------