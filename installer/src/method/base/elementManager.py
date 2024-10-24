# coding: utf-8
# $$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$

# $$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$
# import
import time
from selenium.webdriver.chrome.webdriver import WebDriver
from datetime import datetime
from typing import Dict, Any, List, Tuple

# 自作モジュール
from .utils import Logger
from const import NGWordList, Address
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

    def updateSubDict(self, dictBox: Dict[str, Dict[str, Any]], name: str, inputDict: Dict[str, Any]) -> Dict[str, Dict[str, Any]]:
        dictBox[name].update(inputDict)
        return dictBox


# ----------------------------------------------------------------------------------
# 特定の値だった場合にNoneを返す

    def _returnNoneIfValue(self, value: Any, ifValueList: List):
        for ifValue in ifValueList:
            if value == ifValue:
                return None
            else:
                return value


# ----------------------------------------------------------------------------------
# 要素を繰り返し取得してリストにする
# conditions=[(by, value), (otherBy, otherValue)]のようにtupleのリストを返す


    def _getElementList(self, conditions: List[Tuple[str, str]], ifValueList: List):
        elementList = []
        for by, value in conditions:
            element = self.getElement(by=by, value=value)
            # 特定のリストは除外する
            element = self._returnNoneIfValue(value=element, ifValueList=ifValueList)
            elementList.append(element)
        return elementList


# ----------------------------------------------------------------------------------
