# coding: utf-8
# $$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$

# $$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$
# import


# $$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$
# **********************************************************************************


class TableSchemas:


# ----------------------------------------------------------------------------------
# サブ辞書

    COOKIES_TABLE_COLUMNS = {
        "id": "INTEGER PRIMARY KEY AUTOINCREMENT",
        "name": "TEXT NOT NULL",
        "value": "TEXT NOT NULL",
        "domain": "TEXT",
        "path": "TEXT",
        "expires": "INTEGER",
        "maxAge": "INTEGER",
        "createTime": "INTEGER NOT NULL",
    }


# ----------------------------------------------------------------------------------
# サブ辞書
# priorityは優先順位→若い番号ほど順位が高い


    TEXT_TABLE_COLUMNS = {
        "id": "INTEGER PRIMARY KEY AUTOINCREMENT",
        "name": "TEXT NOT NULL",
        "createTime": "TEXT NOT NULL",
        "url": "TEXT NOT NULL",
        "trainLine": "TEXT NOT NULL",
        "station": "TEXT NOT NULL",
        "walking": "TEXT NOT NULL",
        "ad": "TEXT NOT NULL",
        "area": "TEXT NOT NULL",
        "item": "TEXT NOT NULL",
        "address": "TEXT NOT NULL",
        "rent": "TEXT NOT NULL",
        "managementCost": "TEXT NOT NULL",

        "secondComment": "TEXT",
        "thirdComment": "TEXT",
        "fourthComment": "TEXT",
        "selectItems": "TEXT",
    }


# ----------------------------------------------------------------------------------
# サブ辞書

    IMAGE_TABLE_COLUMNS = {
        "id": "INTEGER PRIMARY KEY",
        "name": "TEXT NOT NULL",
        "createTime": "TEXT NOT NULL",
        "currentUrl": "TEXT NOT NULL",
        "間取り図": "TEXT NOT NULL",
        "外観写真": "TEXT NOT NULL",
        "玄関": "TEXT",
        "リビング": "TEXT",
        "キッチン": "TEXT",
        "ベッドルーム": "TEXT",
        "風呂画像": "TEXT",
        "エントランス": "TEXT",
        "セキュリティ": "TEXT",
        "ロビー": "TEXT",
        "宅配BOX": "TEXT",
        "駐輪場": "TEXT",
        "洗面所": "TEXT",
        "トイレ": "TEXT",
        "ウォークインクロゼット": "TEXT",
        "リビングルーム": "TEXT",
        "シューズインクローゼット": "TEXT",
        "周辺画像": "TEXT",
        "他共有部分": "TEXT",
        "他設備": "TEXT",
        "その他": "TEXT",
        "収納": "TEXT",
    }


# ----------------------------------------------------------------------------------
#* メイン辞書

    TABLE_PATTERN = {
        "cookiesDB": COOKIES_TABLE_COLUMNS,
        "text": TEXT_TABLE_COLUMNS,
        "image": IMAGE_TABLE_COLUMNS
    }


# ----------------------------------------------------------------------------------
