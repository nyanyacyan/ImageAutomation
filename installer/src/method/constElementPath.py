# coding: utf-8
# $$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$

# $$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$
# import
from enum import Enum


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
