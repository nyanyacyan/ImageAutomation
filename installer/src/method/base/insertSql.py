# coding: utf-8
# $$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$

# $$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$
# import
import time, os
from selenium.webdriver.chrome.webdriver import WebDriver
from datetime import datetime
from typing import Dict, Any, List
from dotenv import load_dotenv
from pprint import pprint

from selenium.webdriver.remote.webelement import WebElement
from selenium.common.exceptions import NoSuchElementException


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


class InsertSql:
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

        # newのカウントを行う
        newElement = self._getClassElementList()
        self.logger.warning(f"newElement: {newElement}: {len(newElement)}個の[NEW]の要素を発見")

        data = {}
        for i in range(len(newElement)):
            link = linkList[i].get_attribute('href')
            newText = newElement[i].text
            newTextList = newText.split('\u3000')  # \u3000は全角の空白

            station = newTextList[0] + '駅'
            trainName = newTextList[1]
            walking = newTextList[2]

            stationWord = '  '.join([station, walking])

            data[i + 1] = {
                'link': link,
                'station': station,
                'walking': walking,
                'trainName': trainName,
                'stationWord': stationWord,
            }

            pprint(data[i + 1])
        print(f"data:\n{data}")

        # もしリンク数と「new」が正の場合には次のページに行って再度実施

        # もしリンク数と「new」が誤の場合には完了


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

            pprint(f"updateColumnsData: {updateColumnsData}")

            # 生成したコメントをSQLiteへ格納（アップデート）
            self._updateDataInSQlite(id=id, updateColumnsData=updateColumnsData)

            # 詳細ページから画像データを取得
            imageDict = self._mergeImageTableData(id=id, mergeDict=mergeDict)

            # imageデータをSQLiteへ入れ込む
            id = self._ImageInsertData(imageDict=imageDict)

            # debug確認
            self.SQLite.getRecordsAllData(tableName=self.textTableName)

            # debug確認
            self.SQLite.getRecordsAllData(tableName=self.imageTableName)

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
        self.logger.info(f"imageDataにて使うデータ: {dataInMergeDict}")

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


    def _imagesDict(self):
        # display: noneがあったら解除
        self.element.unlockDisplayNone()

        imageElements = self._getImageList()
        self.logger.info(f"imageElements: {imageElements}")

        imageData = {}
        for element in imageElements:
            imageUrl = element.get_attribute("href")
            self.logger.debug(f"imageUrl: {imageUrl}")

            try:
                # 要素を絞り込み
                imageTag = self.element.filterElement(parentElement=element, by='tag', value='img')
            except NoSuchElementException:
                self.logger.warning(f"<img>タグが見つかりませんでした: {element}")
                continue

            self.logger.info(f"imageTag: {imageTag}")

            imageTitle = imageTag.get_attribute('title') or imageTag.get_attribute('alt')
            self.logger.debug(f"imageTitle: {imageTitle}")

            imageData[imageTitle] = imageUrl

        self.logger.warning(f"imageData:\n{imageData}")

        # image.key()は辞書のKeyオブジェクトを返すためListに変換する必要あり
        imageKeys = list(imageData.keys())
        self.logger.warning(f"imageDataのKey一覧:\n{imageKeys}")

        return imageData


# ----------------------------------------------------------------------------------
# すべての画像データを取得する

    def _getImageList(self):
        return self.element.getElements(
            by="xpath",
            value="//div[@id='box_main_gallery']//li//a"
        )


# ----------------------------------------------------------------------------------
# 特定のクラスの要素をすべて取得する

    def _getClassElementList(self):
        return self.element.getElements(
            by="class",
            value="new"
        )


# ----------------------------------------------------------------------------------
# 一覧ページからすべてのリンクを取得してリストにする

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

        selectItems = self.element.textCleaner(textList=mergeDict['item'])

        # 3ページ目のコメント
        thirdComment = await self.chatGPTComment(
            selectItems=selectItems,
            itemStartValue=0,
            maxlen=100
        )

        # 4ページ目のコメント
        fourthComment = await self.chatGPTComment(
            selectItems=selectItems,
            itemStartValue=4,
            maxlen=100
        )

        return {
            "secondComment": secondComment,
            "thirdComment": thirdComment,
            "fourthComment": fourthComment,
            "selectItems": selectItems,
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
    async def chatGPTComment(self, selectItems: List, itemStartValue: int, maxlen: int):
        prompt = self.ChatGPTPromptCreate(selectItems=selectItems, itemStartValue=itemStartValue, maxlen=maxlen)
        result = await self.chatGPT.resultOutput(
            prompt=prompt,
            fixedPrompt=ChatGptPrompt.fixedPrompt.value,
            endpointUrl=ChatgptUtils.endpointUrl.value,
            model=ChatgptUtils.model.value,
            apiKey=os.getenv('CHATGPT_APIKEY'),
            maxlen=maxlen,
            maxTokens=ChatgptUtils.MaxToken.value
        )
        self.logger.info(f"3ページ目のコメント: {result}")
        self.logger.info(f"3ページ目のコメント文字数: {len(result)}文字")
        return result


# ----------------------------------------------------------------------------------
# Prompt生成
# 文字数制限はここで入力

    @decoInstance.funcBase
    def ChatGPTPromptCreate(self, selectItems: List, itemStartValue: int, maxlen: int):
        # items = self.element.textCleaner(textList=mergeDict['item'])

        self.logger.info(f"selectItems: {selectItems}")

        prompt = ChatGptPrompt.recommend.value.format(
            maxlen=maxlen,
            minLen=maxlen - 20,
            item0=selectItems[itemStartValue],
            item1=selectItems[itemStartValue + 1],
            item2=selectItems[itemStartValue + 2],
            item3=selectItems[itemStartValue + 3],
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
        return secondComment


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
