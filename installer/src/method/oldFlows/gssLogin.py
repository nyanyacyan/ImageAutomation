# coding: utf-8
# ----------------------------------------------------------------------------------
#! ここで定義して「Flow」で扱う
#! 引数はここで基本渡す。


# ----------------------------------------------------------------------------------
import time

# 自作モジュール
from ..base.spreadsheetRead import SpreadsheetRead
from ..base.LoginWithCookie import AutoLogin
from .base.driver_control import Operation
from .base.df_Create import DFCreate
from ..base.utils import Logger


####################################################################################

# スプシから読み込み

class StartSpreadsheetRead(SpreadsheetRead):
    def __init__(self, sheet_url, account_id, debugMode=True):
        super().__init__(sheet_url, account_id, debugMode)


# スプシからurlを読み込む
    def get_url_in_gss(self):
        return super().get_url_in_gss()


# 取得したURLに付属してnameを取得
    def get_name_in_gss(self):
        return super().get_name_in_gss()



####################################################################################


class OverAutoLogin(AutoLogin):
    def __init__(self, chrome, debugMode=True):
        super().__init__(chrome, debugMode)


    def sever_open_site(self, url, notifyFunc):
        by_pattern='id'
        check_path='searchOrder'
        field_name='open_site'
        return super().sever_open_site(url, by_pattern, check_path, notifyFunc, field_name)


    def site_open_title_check(self, gss_url, gss_title, field_name, notifyFunc):
        return super().site_open_title_check(gss_url, gss_title, field_name, notifyFunc)



####################################################################################


class Drop(Operation):
    def __init__(self, chrome, debugMode=True):
        super().__init__(chrome, debugMode)


    def drop_down_select(self, by_pattern, xpath, select_word, field_name='drop_down_select'):
        by_pattern='xpath'
        xpath="//ul[@id='searchOrderList']//a[contains(text(), '新着順')]"
        select_word='新着順'
        return super().drop_down_select(by_pattern, xpath, select_word, field_name)


####################################################################################


class GetData(DFCreate):
    def __init__(self, chrome, debugMode=True):
        super().__init__(chrome, debugMode)


    def _getSiteData(self, by_pattern, xpath, category_info, field_name):
        category_info = [
            ("商品ID", "attribute", "goodsid"),
            ("商品名", "xpath", "//p[@class='itemCard_name']"),
            ("状態", "xpath", "//p[@class='itemCard_status']"),
            ("価格", "xpath", "//p[contains(@class, 'itemCard_price')]")
        ]
        return super()._sort_data(by_pattern, xpath, category_info, field_name)


####################################################################################


class GssLogin:
    def __init__(self, sheet_url, account_id, chrome, debugMode=True) -> None:
        self.chrome = chrome

        self.getLogger = Logger(__name__, debugMode=debugMode)
        self.logger = self.getLogger.getLogger()

        self.sheet_url = sheet_url
        self.account_id = account_id

        # インスタンス化
        self.gss_read = StartSpreadsheetRead(sheet_url=self.sheet_url, account_id=self.account_id, chrome=self.chrome, debugMode=debugMode)
        self.auto_login = OverAutoLogin(chrome=self.chrome, debugMode=debugMode)



    def process(self):
        try:
            self.logger.info(f"***** {self.account_id} process 開始 *****")

            # スプシから情報を取得
            brand_name = self.gss_read._sort_brand_name()
            site_url = self.gss_read._sort_site_url()

            self.logger.debug(f"brand_name: {brand_name}, site_url: {site_url} ")

            time.sleep(2)

            # サイトを開く
            self.auto_login.open_site(site_url)
            self.logger.debug(f"brand_name: {brand_name}, site_url: {site_url} ")


            self.logger.info(f"***** {self.account_id} process 終了 *****")


        except Exception as e:
            self.logger.error(f"{self.account_id} process: 処理中にエラーが発生{e}")


####################################################################################



####################################################################################



####################################################################################
