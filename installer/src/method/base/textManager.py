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
        if isinstance(targetList, list) and len(targetList) == 1 and isinstance(targetList[0], str):
            targetList = targetList[0].split(', ')

        targetList = [word.strip() for word in targetList]
        ngWords = [word.strip() for word in ngWords]

        self.logger.warning(f"\ntargetList: {targetList}\nngWords: {ngWords}")
        self.logger.warning(f"\ntargetList: {len(targetList)}\nngWords: {len(ngWords)}")
        self.logger.warning(f"\ntargetListType: {type(targetList)}\nngWordsType: {type(ngWords)}")

        self.logger.warning(f"targetList: {targetList[0]}\n\nngWords: {ngWords[0]}")

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
