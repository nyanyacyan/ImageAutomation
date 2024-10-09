# coding: utf-8
# $$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$

# $$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$
# import
import time
from selenium.webdriver.chrome.webdriver import WebDriver
from datetime import datetime


# 自作モジュール
from .utils import Logger
from .decorators import Decorators

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


    def getTextAndMeta(self, name: str, by: str, titleBy: str, value: str, titleValue: str, placement: int, priority: int, chatGpt1: str, chatGpt2: str):
        dataDict = {}
        name = name
        date = self.currentDate
        getText = self.getElement(by=by, value=value)
        url = self.chrome.current_url()
        title = self.getElement(by=titleBy, value=titleValue)
        chatGpt1 = "ここに関数をいれる"
        chatGpt1 = "ここに関数をいれる"

        if getText:
            status = "success"
        else:
            status = "failure"

        dataDict[name]={
            "name": name,
            "getText": getText,
            "createTime": date,
            "url": url,
            "title": title,
            "placement": placement,
            "priority": priority,
            "status": status,
            "chatGpt1": chatGpt1,
            "chatGpt2": chatGpt2,
        }

        return dataDict


# ----------------------------------------------------------------------------------
