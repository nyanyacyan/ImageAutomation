# coding: utf-8
# $$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$

# $$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$
# import
from selenium.webdriver.chrome.webdriver import WebDriver


# 自作モジュール
from .utils import Logger


# $$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$
# **********************************************************************************


class ElementManager:
    def __init__(self, chrome: WebDriver, debugMode=True):
        # logger
        self.getLogger = Logger(__name__, debugMode=debugMode)
        self.logger = self.getLogger.getLogger()

        self.chrome = chrome


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


    def inputText(self, by: str, value: str, inputText: str):
        inputElement = self.getElement(by=by, value=value)
        inputElement.send_keys(inputText)


# ----------------------------------------------------------------------------------


    def ClearInputField(self, by: str, value: str):
        element = self.getElement(by=by, value=value)
        element.clear()
        return


# ----------------------------------------------------------------------------------


    def clickElement(self, by: str, value: str):
        element = self.getElement(by=by, value=value)
        element.click()
        return


# ----------------------------------------------------------------------------------
