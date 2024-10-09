# coding: utf-8
# ----------------------------------------------------------------------------------

# ----------------------------------------------------------------------------------
# import
import sys, os


# 自作モジュール
from .utils import Logger


# **********************************************************************************


class TextManager:
    def __init__(self, debugMode=True):

        # logger
        self.getLogger = Logger(__name__, debugMode=debugMode)
        self.logger = self.getLogger.getLogger()


# ----------------------------------------------------------------------------------
# 大元のリストからNGWordを除外したリストを作成

    def filterWords(targetList: list, ngWords: list):
        filterWords = [word for word in targetList if word not in ngWords]
        return filterWords


# ----------------------------------------------------------------------------------
