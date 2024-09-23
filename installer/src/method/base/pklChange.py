# coding: utf-8
# $$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$
# 2023/6/14 更新
# テストOK
# $$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$

# import
import pickle
import pandas as pd
from typing import Any, Callable, Optional


# 自作モジュール
# import const
from .utils import Logger
from .errorHandlers import PickleReadError, PickleWriteError
from .decorators import funcBase
from .path import BaseToPath


# $$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$
# **********************************************************************************


class PickleRead:
    def __init__(self, debugMode=True):

        # logger
        self.getLogger = Logger(__name__, debugMode=debugMode)
        self.logger = self.getLogger.getLogger()

        # インスタンス化
        self.pickleError = PickleReadError(debugMode=debugMode)
        self.path = BaseToPath(debugMode=debugMode)


# ----------------------------------------------------------------------------------
# pickleデータを通常のデータへ変換

    @funcBase
    def pklToUtf8(
            self,
            pklName: str,
            notifyFunc: Optional[Callable[[str], None]] = None,
            levelsUp: int = 4,
            dirName: str = 'resultOutput',
            subDirName: str = 'pickles'
        ):
        try:
            fullpath = self.path.getPickleFilePath(pklName=pklName, levelsUp=levelsUp, dirName=dirName, subDirName=subDirName)

            with open(f'{fullpath}.pkl', 'rb') as f:
                loadData = pickle.load(f)
                self.logger.info(f"pickleFile取得、完了: {pklName}")
            return loadData

        except Exception as e:
            self.pickleError.pickleErrorHandler(fileName=pklName, e=e, notifyFunc=notifyFunc)


# ----------------------------------------------------------------------------------
# pickleデータよりDataFrameを復元

    @funcBase
    def pickleToDf(
        self,
        pklName: str,
        notifyFunc: Optional[Callable[[str], None]] = None,
        levelsUp: int = 4,
        dirName: str = 'resultOutput',
        subDirName: str = 'pickles'
    ):
        try:
            fullpath = self.path.getPickleFilePath(pklName=pklName, levelsUp=levelsUp, dirName=dirName, subDirName=subDirName)

            pklToDf = pd.read_pickle(fullpath)
            self.logger.debug(f"pklToDf: \n{pklToDf.head()}")

            self.logger.info(f"pickleからdfへの復元、完了: {pklName}")

            return pklToDf

        except Exception as e:
            self.pickleError.pickleErrorHandler(fileName=pklName, e=e, notifyFunc=notifyFunc)


# ----------------------------------------------------------------------------------
# **********************************************************************************


class PickleWrite:
    def __init__(self, debugMode=True):

        # logger
        self.getLogger = Logger(__name__, debugMode=debugMode)
        self.logger = self.getLogger.getLogger()

        # インスタンス
        self.path = BaseToPath(debugMode=debugMode)
        self.pickleError = PickleWriteError(debugMode=debugMode)


# ----------------------------------------------------------------------------------
# pickleデータへの変換

    @funcBase
    def toPkl(
        self,
        data: Any,
        pklName: str,
        levelsUp: int = 4,
        dirName: str = 'resultOutput',
        subDirName: str = 'pickles',
        notifyFunc: Optional[Callable[[str], None]] = None
    ):
        try:
            fullpath = self.path.getPickleFilePath(pklName=pklName, levelsUp=levelsUp, dirName=dirName, subDirName=subDirName)

            with open(f'{fullpath}.pkl', 'wb') as f:
                pickle.dump(data, f)
                self.logger.info(f"{pklName}:pickleに保存完了")

        except Exception as e:
            self.pickleError.handler(fileName=pklName, e=e, notifyFunc=notifyFunc)


# ----------------------------------------------------------------------------------
# DataFrameからpickleデータへ変換

    @funcBase
    def dfToPickle(
        self,
        df: pd.DataFrame,
        pklName: str,
        levelsUp: int = 4,
        dirName: str = 'resultOutput',
        subDirName: str = 'pickles',
        notifyFunc: Optional[Callable[[str], None]] = None

    ):
        try:
            fullpath = self.path.getPickleFilePath(pklName=pklName, levelsUp=levelsUp, dirName=dirName, subDirName=subDirName)

            if not df.empty:
                df.to_pickle(fullpath)
                self.logger.info(f"{pklName}:pickleに保存完了")

        except Exception as e:
            self.pickleError.handler(fileName=pklName, e=e, notifyFunc=notifyFunc)


# ----------------------------------------------------------------------------------
# **********************************************************************************

