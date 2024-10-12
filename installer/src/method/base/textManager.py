# coding: utf-8
# ----------------------------------------------------------------------------------

# ----------------------------------------------------------------------------------
# import
import sys, os
from typing import List


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

    def filterWords(self, targetList: list, ngWords: list):
        filterWords = [word for word in targetList if word not in ngWords]
        return filterWords


# ----------------------------------------------------------------------------------
# テキストを複数結合させる(Noneは除外する)

    def textJoin(self, joinWordsList: list, joint: str = ''):
        result = filter(None, joinWordsList)
        return joint.join(result)


# ----------------------------------------------------------------------------------
# リストの最初にテキストを追加

    def addListFirstLast(self, lst: List, firstWord: str, lastWord: str):
        lst.insert(0, firstWord)
        lst.append(lastWord)
        return lst

# ----------------------------------------------------------------------------------
