# coding: utf-8
# $$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$
# 2023/9/14 更新
# テストOK
# $$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$

# import
import os
from pathlib import Path
from datetime import datetime

# 自作モジュール
# import const
from .utils import Logger
from .errorHandlers import AccessFileNotFoundError



# $$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$
# **********************************************************************************
# 利用するメソッドがBaseだったときのクラス

class BaseToPath:
    def __init__(self, debugMode=True):

        # logger
        self.getLogger = Logger(__name__, debugMode=debugMode)
        self.logger = self.getLogger.getLogger()

        # インスタンス
        self.fileNotFoundError = AccessFileNotFoundError(debugMode=debugMode)
        self.currentDate = datetime.now().strftime('%y%m%d')


# ----------------------------------------------------------------------------------
# logsFileを取得

    def toLogsPath(self, levelsUp: int = 4, dirName: str = 'resultOutput', subDirName: str = 'logs'):
        resultOutputPath = self.getResultOutputPath(levelsUp=levelsUp, dirName=dirName)

        logsPath = resultOutputPath / subDirName / self.currentDate

        self.isDirectoryExists(path=logsPath)
        self.logger.debug(f"logsPath: {logsPath}")

        return logsPath


# ----------------------------------------------------------------------------------
# inputDataの中にあるFilePathを取得

    def getInputDataFilePath(self, fileName: str, levelsUp: int = 2, dirName: str = 'inputData'):
        try:
            inputDataPath = self.getInputDataPath(levelsUp=levelsUp, dirName=dirName)

            accessFilePath = inputDataPath / fileName
            self.logger.debug(f"{fileName} を発見: {accessFilePath}")

            return accessFilePath

        except Exception as e:
            self.fileNotFoundError.accessFileNotFoundError(fileName=fileName, e=e)

# ----------------------------------------------------------------------------------
# pickleFileを取得

    def getPickleFilePath(self, pklName: str, levelsUp: int = 4, dirName: str = 'resultOutput', subDirName: str = 'pickles'):
        picklesPath = self.toPicklesPath(levelsUp=levelsUp, dirName=dirName, subDirName=subDirName)

        pickleFilePath = picklesPath / f'{pklName}.pkl'
        self.logger.debug(f"pickleFilePath: {pickleFilePath}")

        return pickleFilePath


# ----------------------------------------------------------------------------------


    @property
    def currentDir(self):
        currentDirPath = Path(__file__).resolve()
        return currentDirPath


# ----------------------------------------------------------------------------------


    def getResultOutputPath(self, levelsUp: int = 4, dirName: str = 'resultOutput'):
        currentDirPath = self.currentDir

        # スタートが0で1つ上の階層にするため→levelsUpに１をいれたら１個上の階層にするため
        resultOutputPath = currentDirPath.parents[levelsUp - 1] / dirName
        self.logger.debug(f"{dirName}: {resultOutputPath}")
        return resultOutputPath


# ----------------------------------------------------------------------------------
# File名を付け足して書込時に拡張子を付け足す


    def getWriteFilePath(self, fileName: str, levelsUp: int = 4, dirName: str = 'resultOutput'):
        resultOutputPath = self.getResultOutputPath(levelsUp=levelsUp, dirName=dirName)
        filePath = resultOutputPath / fileName
        return filePath


# ----------------------------------------------------------------------------------
# ディレクトリがない可能性の箇所に貼る関数

    def isDirectoryExists(self, path: Path):
        if not path.exists():
            # 親のディレクトリも作成、指定していたディレクトリが存在してもエラーを出さない
            path.mkdir(parents=True, exist_ok=True)
            self.logger.info(f"{path.name} がないため作成")
        else:
            self.logger.debug(f"{path.name} 発見")
        return path


# ----------------------------------------------------------------------------------
# pickle格納の場所へのPath

    def toPicklesPath(self, levelsUp: int = 4, dirName: str = 'resultOutput', subDirName: str = 'pickles'):
        resultOutputPath = self.getResultOutputPath(levelsUp=levelsUp, dirName=dirName)

        picklesPath = resultOutputPath / subDirName

        self.isDirectoryExists(path=picklesPath)
        self.logger.debug(f"picklesPath: {picklesPath}")

        return picklesPath


# ----------------------------------------------------------------------------------

# # inputDataへのPath

    def getInputDataPath(self, levelsUp: int = 2, dirName: str = 'inputData'):
        currentDirPath = self.currentDir

        # スタートが0で1つ上の階層にするため→levelsUpに１をいれたら１個上の階層にするため
        inputDataPath = currentDirPath.parents[levelsUp - 1] / dirName
        self.logger.debug(f"{dirName}: {inputDataPath}")
        return inputDataPath


# ----------------------------------------------------------------------------------
# File名を付け足して書込時に拡張子を付け足す

    def getReadFilePath(self, fileName: str, levelsUp: int = 2, dirName: str = 'inputData'):
        inputDataPath = self.getInputDataPath(levelsUp=levelsUp, dirName=dirName)

        FilePath = inputDataPath / fileName
        self.logger.debug(f"FilePath: {FilePath}")

        return FilePath


# ----------------------------------------------------------------------------------
# File名を付け足して書込時に拡張子を付け足す

    def getInputDataFilePath(self, fileName: str, levelsUp: int = 2, dirName: str = 'inputData'):
        resultOutputPath = self.getResultOutputPath(levelsUp=levelsUp, dirName=dirName)

        FilePath = resultOutputPath / fileName
        self.logger.debug(f"FilePath: {FilePath}")

        return FilePath


# ----------------------------------------------------------------------------------


    def writeFileDateNamePath(self, extension: str, subDirName: str, levelsUp: int = 4, dirName: str = 'resultOutput'):
        resultOutputPath = self.getResultOutputPath(levelsUp=levelsUp, dirName=dirName)
        fileFullPath = os.path.join(resultOutputPath, subDirName, f'{self.currentDate}{extension}')
        self.logger.debug(f"fileFullPath: {fileFullPath}")
        return fileFullPath


# ----------------------------------------------------------------------------------
# cookies格納の場所へのPath

    def writeCookiesFileDateNamePath(self, extension: str, levelsUp: int = 4, dirName: str = 'resultOutput', subDirName: str = 'cookies'):
        resultOutputPath = self.getResultOutputPath(levelsUp=levelsUp, dirName=dirName)
        fileFullPath = os.path.join(resultOutputPath, subDirName, f'{self.currentDate}{extension}')
        self.logger.debug(f"fileFullPath: {fileFullPath}")
        return fileFullPath


# ----------------------------------------------------------------------------------