# coding: utf-8
# $$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$

# $$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$
# import
import os
from enum import Enum
from dotenv import load_dotenv

load_dotenv()


# $$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$
# **********************************************************************************


class ElementSpecify(Enum):
    ID='id'
    XPATH='xpath'
    CSS='css'


# **********************************************************************************


class ElementPath(Enum):


# ----------------------------------------------------------------------------------
# flowMoveGetElement

    # 検索画面の消去する
    SEARCH_DELETE_BTN_PATH="//a[@class='w_close']"


    # 詳細ページの要素（.formatにて追記することで引数に充当）
    DETAIL_PAGE_BTN_PATH="//a[text()='物件画像'])[{}]"  # すべての//a[text()='物件画像']を取得→1個目


# ----------------------------------------------------------------------------------
# _listPageInfo

    STATION_VALUE="//div[@class='searchResultLsit'][{}]//tr[@class='searchResultLsitTabTr1']//div[@class='vicinityInfo']/p[@class='new']/span[1]"

    TRAIN_LINE="//div[@class='searchResultLsit'][{}]//tr[@class='searchResultLsitTabTr1']//div[@class='vicinityInfo']/p[@class='new']/span[2]"

    WAKING="//div[@class='searchResultLsit'][{}]//tr[@class='searchResultLsitTabTr1']//div[@class='vicinityInfo']/p[@class='new']/span[3]"


# ----------------------------------------------------------------------------------
# _detailPageInfo


    NAME="//th[text()='物件名']/following-sibling::td[1]/span"

    AD="//th[text()='広告可否']/following-sibling::td[1]/span"

    AREA="//th[text()='専有面積']/following-sibling::td[1]/span"

    ITEM="//th[text()='広告可否']/following-sibling::td[1]/span"

    ADDRESS="//th[text()='物件所在地']/following-sibling::td[1]/span"

    RENT="//th[text()='賃料']/following-sibling::td[1]/span"

    MANAGEMENT_COST="//th[text()='管理費等']/following-sibling::td[1]/span"



# ----------------------------------------------------------------------------------
# ここでos.getenv("PASS")を定義してしまうと実行してしまう関係からここでは呼び出さない

class LoginElement(Enum):
    LOGIN_INFO = {
        "idBy": "id",
        "idValue": "username",
        "passBy": "id",
        "passValue": "password",
        "btnBy": "name",
        "btnValue": "action",
        "bypassIdBy": "xpath",
        "bypassIdValue": "//a[text()='いい生活アカウントでログイン']",
        "modalBy" : "xpath",
        "modalValue": "//a[@class='w_close']",
    }


    BYPASS_SITE_INFO = {
        'by': 'xpath',
        'value': "//a[text()='いい生活アカウントでログイン']"
    }

# ----------------------------------------------------------------------------------


class ImageInfo(Enum):
    #! 修正必要
    BASE_IMAGE_PATH = {
        "A": "/Users/nyanyacyan/Desktop/Project_file/ImageAutomation/installer/src/method/inputData/A.png",
        "B": "/Users/nyanyacyan/Desktop/Project_file/ImageAutomation/installer/src/method/inputData/B.png",
        "C": "/Users/nyanyacyan/Desktop/Project_file/ImageAutomation/installer/src/method/inputData/C.png",
        "D": "/Users/nyanyacyan/Desktop/Project_file/ImageAutomation/installer/src/method/inputData/D.png",
    }

    BASE_IMAGE_SIZE = (1080, 1080)

    FONT_SIZES = {
        "A": 75,
        "B": 30,
        "C": 30,
        "D": 30,
    }

    #! 修正必要

    FONT_PATH = "/Users/nyanyacyan/Desktop/project_file/ImageAutomation/installer/src/method/inputData/NotoSansJP-VariableFont_wght.ttf"


    #! 修正必要
    OUTPUT_PATH = "/Users/nyanyacyan/Desktop/project_file/ImageAutomation/installer/resultOutput"


    IMAGE_NUM = {
        "A": "1",
        "B": "2",
        "C": "2",
        "D": "2",
    }

    POSITIONS = {
        "A": {
            "IMAGE_CENTER": (0, 83, 1080, 998),
            "TEXT_RIGHT_TOP": (920, 150, 1020, 550),
            "TEXT_RIGHT_BOTTOM": (920, 600, 1020, 1000),
            "TEXT_BOTTOM": (150, 870, 550, 950),
        },
        "B": {
            "IMAGE_TOP_LEFT": (0, 180, 550, 500),
            "IMAGE_BOTTOM_LEFT": (0, 550, 450, 950),
            "TEXT_TOP_RIGHT": (570, 180, 1080, 500),
            "TEXT_BOTTOM_RIGHT": (745, 620, 975, 850)
        },
        "C": {
            "IMAGE_TOP_LEFT": (0, 175, 550, 500),
            "IMAGE_BOTTOM_LEFT": (0, 550, 450, 950),
            "TEXT_TOP_RIGHT": (570, 175, 1080, 440),
            "TEXT_BOTTOM_RIGHT": (800, 550, 1010, 760)
        },
        "D": {
            "IMAGE_TOP_LEFT": (0, 175, 550, 550),
            "IMAGE_BOTTOM_LEFT": (0, 580, 500, 988),
            "TEXT_TOP_RIGHT": (570, 175, 1080, 440),
            "TEXT_BOTTOM_RIGHT": (765, 530, 995, 760)
        }
    }




    TOP_MAX_WIDTH = 120
    TOP_LINE_HEIGHT = 200
    MAX_WIDTH = 300
    LINE_HEIGHT = 30


    FILL_COLOR_BLACK = (0, 0, 0)
    FILL_COLOR_GREEN = (0, 255, 0)
    FILL_COLOR_WHITE = (255, 255, 255)


    TOP_IMAGE_SIZE = (700, 1300)
    IMAGE_SIZE = (300, 300)
    IMAGE_SIZE_SMALL = (150, 150)



# ----------------------------------------------------------------------------------
