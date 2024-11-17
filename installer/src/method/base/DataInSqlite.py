# coding: utf-8
# $$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$

# $$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$
# import
import time, os
from selenium.webdriver.chrome.webdriver import WebDriver
from datetime import datetime
from typing import Dict, Any
from dotenv import load_dotenv

from selenium.webdriver.remote.webelement import WebElement


# 自作モジュール
from .utils import Logger
from .elementManager import ElementManager
from .AiOrder import ChatGPTOrder
from .textManager import TextManager
from dataclass import ListPageInfo, DetailPageInfo
from .SQLite import SQLite
from .decorators import Decorators
from .jumpTargetPage import JumpTargetPage
from const import ChatGptPrompt, ChatgptUtils, TableName
from constElementPath import ElementPath, ElementSpecify
from constSqliteTable import TableSchemas

decoInstance = Decorators(debugMode=True)

load_dotenv()

# $$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$
# **********************************************************************************


class DataInSQLite:
    def __init__(self, chrome: WebDriver, debugMode=True):
        # logger
        self.getLogger = Logger(__name__, debugMode=debugMode)
        self.logger = self.getLogger.getLogger()

        self.chrome = chrome

        # テーブルName
        self.textTableName = TableName.TEXT.value
        self.imageTableName = TableName.IMAGE.value

        self.currentDate = datetime.now().strftime('%y%m%d_%H%M%S')
        self.element = ElementManager(chrome=self.chrome, debugMode=debugMode)
        self.chatGPT = ChatGPTOrder(debugMode=debugMode)
        self.textManager = TextManager(debugMode=debugMode)
        self.SQLite = SQLite(debugMode=debugMode)
        self.jumpTargetPage = JumpTargetPage(chrome=self.chrome, debugMode=debugMode)


# ----------------------------------------------------------------------------------
# flow
# 一覧の物件リストから詳細ページへ移動して取得する

    @decoInstance.funcBase
    async def flowCollectElementDataToSQLite(self,retryCount: int = 5, delay: int = 2):

        # ジャンプしてURLへ移動して検索画面を消去まで実施
        self._navigateToTargetPage(delay=delay)

        # 一覧ページにある物件詳細リンクを全て取得
        linkList = self._getLinkList()
        self.logger.warning(f"linkList: {linkList}: {len(linkList)}個のリンクを取得")

        allList = []
        allIDList = []
        for i in range(retryCount):
            # 一覧ページからスクレイピング
            listPageInfo = self._getListPageData(tableValue=(i + 1))

            # webElementをtext化
            fixedListPageInfo = self.webElementToText(webElementData=listPageInfo)
            self.logger.warning(f"listPageInfo: {fixedListPageInfo}")

            # 物件詳細リンクにアクセス
            linkList[i].click()
            time.sleep(delay)

            # すべてのタブ（ウィンドウ）ハンドルを取得
            all_handles = self.chrome.window_handles
            self.chrome.switch_to.window(all_handles[-1])

            # 詳細からtextデータをスクレイピング
            detailPageInfo = self._getDetailPageData()

            # webElementをtext化
            fixedDetailPageInfo = self.webElementToText(webElementData=detailPageInfo)
            self.logger.warning(f"fixedDetailPageInfo: {fixedDetailPageInfo}")

            # 取得したtextデータをマージ
            mergeDict = {**fixedListPageInfo, **fixedDetailPageInfo}

            # textデータをSQLiteへ入れ込む
            id = self._textInsertData(mergeDict=mergeDict)

            # ２〜４枚目に必要なコメントを生成
            updateColumnsData = await self._generateComments(mergeDict=mergeDict)

            # 生成したコメントをSQLiteへ格納（アップデート）
            self._updateDataInSQlite(id=id, updateColumnsData=updateColumnsData)

            # mergeDictを更新
            mergeDict.update(updateColumnsData)

            # 詳細ページから画像データを取得
            imageDict = self._mergeImageTableData(id=id, mergeDict=mergeDict)

            # imageデータをSQLiteへ入れ込む
            id = self._ImageInsertData(imageDict=imageDict)

            # それぞれのリストに追加
            allList.append(mergeDict)
            allIDList.append(id)
            time.sleep(delay)

            # 一覧へ戻る
            self.chrome.back()

            self.logger.info(f"{i + 1}回目実施完了")
        self.logger.warning(f"insertID: {allIDList}")
        self.logger.warning(f"allList:\n{allList}")


        return allIDList


# ----------------------------------------------------------------------------------
# webElementのTextを抽出して辞書に組み替える
# 値がwebElementだったら[element.text]をかける

    def webElementToText(self, webElementData: dict):
        return {key: element.text if isinstance(element, WebElement) else element for key, element in webElementData.items()}


# ----------------------------------------------------------------------------------
# 2つの辞書データをマージさせる

    def _mergeImageTableData(self, id: int, mergeDict: Dict):
        dataInMergeDict = self._getImageTableToColInMergeData(id=id, mergeDict=mergeDict)
        imageDict = self._imagesDict()

        return {**dataInMergeDict, **imageDict}


# ----------------------------------------------------------------------------------
# mergeDataに有るImageDataに必要データを取得

    def _getImageTableToColInMergeData(self, id: int, mergeDict: Dict):
        self.logger.debug(f"mergeDict: {mergeDict}")

        name = mergeDict['name']
        createTime = mergeDict['createTime']
        currentUrl = mergeDict['url']

        return {
            "id": id,
            "name": name,
            "createTime": createTime,
            "currentUrl": currentUrl
        }


# ----------------------------------------------------------------------------------
#TODO ElementPathから取得するようにする


    def _imagesDict(self):
        imageElements = self._getImageList()

        imageData = {}
        for element in imageElements:
            imageUrl = element.get_attribute("href")

            imageTag = self.element.getElement(
                by="tag",
                value="img"
            )
            imageTitle = imageTag.get_attribute('title')

            imageData[imageTitle] = imageUrl

        self.logger.warning(f"imageData:\n{imageData}")

        # image.key()は辞書のKeyオブジェクトを返すためListに変換する必要あり
        imageKeys = [list(image.key())[0] for image in imageData]
        self.logger.warning(f"imageDataのKey一覧:\n{imageKeys}")

        return imageData


# ----------------------------------------------------------------------------------
#TODO ElementPathから取得するようにする

    def _getImageList(self):
        return self.element.getElements(
            by="xpath",
            value="//div[@id='box_main_gallery']//li//a"
        )


# ----------------------------------------------------------------------------------
# 一覧ページからすべてのリンクを取得してリストにする
#TODO ElementPathから取得するようにする

    @decoInstance.funcBase
    def _getLinkList(self):
        linkList = self.element.getElements(
            by="xpath",
            value="//a[contains(text(), '物件画像')]"
        )
        return linkList


# ----------------------------------------------------------------------------------
# 入力を実行。入力先のIDを返す

    @decoInstance.funcBase
    def _textInsertData(self, mergeDict: Dict):
        self.SQLite.checkTableExists()

        id = self.SQLite.insertDictData(tableName=self.textTableName, inputDict=mergeDict)
        return id


# ----------------------------------------------------------------------------------
# 入力を実行。入力先のIDを返す

    @decoInstance.funcBase
    def _ImageInsertData(self, imageDict: Dict):
        id = self.SQLite.insertDictData(tableName=self.imageTableName, inputDict=imageDict)
        return id


# ----------------------------------------------------------------------------------
# # 指定のIDのcolumnを指定してアップデートする

    @decoInstance.funcBase
    def _updateDataInSQlite(self, id: int, updateColumnsData: Dict):
        # self.SQLite.checkTableExists()

        self.SQLite.updateData(
            tableName=self.textTableName,
            updateColumnsData=updateColumnsData,
            rowId=id
        )
        return id



# ----------------------------------------------------------------------------------
# tableValueは一覧の中の何個目かどうか

    @decoInstance.funcBase
    def _getListPageData(self, tableValue: Any):
        listPageInfo = self._listPageInfo(tableValue=tableValue)
        return listPageInfo


# ----------------------------------------------------------------------------------


    @decoInstance.funcBase
    def _getDetailPageData(self):
        metaInfo = self._metaInfo()
        detailPageInfo = self._detailPageInfo()
        return {**metaInfo, **detailPageInfo}


# ----------------------------------------------------------------------------------

    @decoInstance.funcBase
    async def _generateComments(self, mergeDict: Dict):
        # 2ページ目のコメント
        secondComment = self.createSecondPageComment(mergeDict=mergeDict)

        print(f"mergeDict: {mergeDict}")

        # 3ページ目のコメント
        thirdComment = await self.chatGPTComment(
            mergeDict=mergeDict,
            itemStartValue=5,
            itemEndValue=8,
            maxlen=30
        )

        print(f"thirdComment: {dict(thirdComment)}")


        # 4ページ目のコメント
        fourthPrompt = await self.chatGPTComment(
            mergeDict=mergeDict,
            itemStartValue=9,
            itemEndValue=12,
            maxlen=30
        )

        print(f"fourthPrompt: {dict(fourthPrompt)}")

        return {
            "secondComment": secondComment,
            "thirdComment": thirdComment,
            "fourthPrompt": fourthPrompt
        }


# ----------------------------------------------------------------------------------


    @decoInstance.funcBase
    def _navigateToTargetPage(self, delay: int):
        # self.jumpTargetPage.flowJumpTargetPage(targetUrl=targetUrl)
        # time.sleep(delay)

        # 念の為、Refresh
        self.chrome.refresh()
        time.sleep(delay)

        # 検索画面を消去
        self.element.clickElement(
            by=ElementSpecify.XPATH.value,
            value=ElementPath.SEARCH_DELETE_BTN_PATH.value
        )
        time.sleep(delay)
        self.logger.debug(f"新しいページに移動後、Refresh完了")


# ----------------------------------------------------------------------------------
# 3ページ目のChatGPT

    @decoInstance.funcBase
    async def chatGPTComment(self, mergeDict: Dict, itemStartValue: int, itemEndValue: int, maxlen: int):
        prompt = self.ChatGPTPromptCreate(mergeDict=mergeDict, itemStartValue=itemStartValue, itemEndValue=itemEndValue, maxlen=maxlen)
        await self.chatGPT.resultOutput(
            prompt=prompt,
            fixedPrompt=ChatGptPrompt.fixedPrompt.value,
            endpointUrl=ChatgptUtils.endpointUrl.value,
            model=ChatgptUtils.model.value,
            apiKey=os.getenv('CHATGPT_APIKEY'),
            maxlen=maxlen,
            maxTokens=ChatgptUtils.MaxToken.value
        )


# ----------------------------------------------------------------------------------
# Prompt生成
# 文字数制限はここで入力

    @decoInstance.funcBase
    def ChatGPTPromptCreate(self, mergeDict: Dict, itemStartValue: int, itemEndValue: int, maxlen: int):
        # 文字列をリストに変換
        if isinstance(mergeDict['item'], str):
            mergeDict['item'] = mergeDict['item'].split(', ')

        # デバッグ用の出力
        print(f"item (after split): {mergeDict['item']}")

        items = [mergeDict['item'][i] for i in range(itemStartValue, itemEndValue + 1)]
        print(f"item: {mergeDict['item']}")
        print(f"items: {items}")
        prompt = ChatGptPrompt.recommend.value.format(
            maxlen=maxlen,
            item0=items[0],
            item1=items[1],
            item2=items[2],
            item3=items[3],
        )

        self.logger.info(f"prompt: {prompt}")

        return prompt


# ----------------------------------------------------------------------------------
# 2ページ目のコメント作成

    @decoInstance.funcBase
    def createSecondPageComment(self, mergeDict: str):
        # 2枚目コメント→つなぎ合わせたもの
        result = self.SQLite.getSortColOneData(
            tableName = self.textTableName,
            primaryKeyCol = "name",
            sortCol = 'createTime',
            primaryKeyColValue = mergeDict.get('name'),
            cols=['trainLine', 'station', 'walking', 'rent', 'managementCost']
        )

        resultDict = dict(result)

        print(f"result: {resultDict}")

        trainLine = resultDict.get('trainLine', '-')
        station = resultDict.get('station', '-')
        walking = resultDict.get('walking', '-')
        rent = resultDict.get('rent', '-')
        managementCost = resultDict.get('managementCost', '-')

        commentParts = [
            "今回は",
            f"{trainLine} の {station}駅 から {walking} の物件です。",
            f"賃料は {rent}",
            f"管理費等は {managementCost}",
            "紹介するよ"
        ]

        self.logger.info(f"secondComment:\n{commentParts}")

        secondComment = '\n'.join(commentParts)
        return {'secondComment': secondComment}


# ----------------------------------------------------------------------------------
# # 一覧ページから取得
# tableValueは何個目かどうか

    @decoInstance.funcBase
    def _listPageInfo(self, tableValue: int) -> Dict[str, WebElement]:
        listInstance = self._listPageInfoValue(tableValue)
        return self._getListPageElement(listPageInfo=listInstance)


# ----------------------------------------------------------------------------------
# 詳細ページからデータを取得

    @decoInstance.funcBase
    def _detailPageInfo(self) -> Dict[str, WebElement]:
        detailInstance = self._detailPageInfoValue()
        return self._getDetailPageElement(detailPageInfo=detailInstance)


# ----------------------------------------------------------------------------------


    def _metaInfo(self):
        currentUrl = self.chrome.current_url
        currentDate = self.currentDate

        dataDict = {
            "url": currentUrl,
            "createTime": currentDate
        }
        return dataDict


# ----------------------------------------------------------------------------------
# tableValueは何個目かどうか

    def _listPageInfoValue(self, tableValue: int):
        return ListPageInfo(
            stationBy=ElementSpecify.XPATH.value,
            stationValue=ElementPath.STATION_VALUE.value.format(tableValue),
            trainLineBy=ElementSpecify.XPATH.value,
            trainLineValue=ElementPath.TRAIN_LINE.value.format(tableValue),
            walkingBy=ElementSpecify.XPATH.value,
            walkingValue=ElementPath.WAKING.value.format(tableValue),
        )


# ----------------------------------------------------------------------------------


    def _detailPageInfoValue(self):
        return DetailPageInfo(
            nameBy=ElementSpecify.XPATH.value,
            nameValue=ElementPath.NAME.value,
            adBy=ElementSpecify.XPATH.value,
            adValue=ElementPath.AD.value,
            areaBy=ElementSpecify.XPATH.value,
            areaValue=ElementPath.AREA.value,
            itemBy=ElementSpecify.XPATH.value,
            itemValue=ElementPath.ITEM.value,
            addressBy=ElementSpecify.XPATH.value,
            addressValue=ElementPath.ADDRESS.value,
            rentBy=ElementSpecify.XPATH.value,
            rentValue=ElementPath.RENT.value,
            managementCostBy=ElementSpecify.XPATH.value,
            managementCostValue=ElementPath.MANAGEMENT_COST.value,
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
    def _getDetailPageElement(self, detailPageInfo: DetailPageInfo) -> Dict[str, WebElement]:
        # html = self.chrome.page_source
        # self.logger.info(f"html: \n{html}")

        name = self.element.getElement(by=detailPageInfo.nameBy, value=detailPageInfo.nameValue)
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
