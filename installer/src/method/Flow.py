# coding: utf-8
# $$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$
# 2024/9/23 更新

# sudo tree /Users/nyanyacyan/Desktop/Project_file/SNS_auto_upper -I 'venv|pyvenv.cfg|__pycache__'


# $$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$
# import
from dotenv import load_dotenv

# 自作モジュール
from .base.utils import Logger
from .

load_dotenv()

# $$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$
# **********************************************************************************
# 一連の流れ

class Flow:
    def __init__(self, debugMode=True):

        # logger
        self.getLogger = Logger(__name__, debugMode=debugMode)
        self.logger = self.getLogger.getLogger()

        # インスタンス



# ----------------------------------------------------------------------------------




# TODO GitHubの整理
# TODO ログイン


# TODO ログインクラスのリファクタリング
# TODO Clickなどのアクションもリファクタリング

# TODO 明和管財サイトへアクセス

# TODO 賃貸仲介会社様はこちらをクリック

# TODO ログインをクリック

# TODO いい生活アカウントでアクセスをクリック

# TODO 路線検索をクリック

# TODO 検索画面を閉じるをクリック

# TODO 詳細をクリック（上から順番に）

# TODO 写真の取得（優先順位を決めて取得）

# TODO 文字列の取得（優先順位を決めて取得）

# TODO データ保管

# TODO 一つ前の画面へ戻る

# TODO batFileの作成→実行、install

# TODO 手順書の作成




# ----------------------------------------------------------------------------------
