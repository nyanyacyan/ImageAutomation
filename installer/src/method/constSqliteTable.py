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
        "chatGpt1": "TEXT",
        "chatGpt2": "TEXT",
    }


# ----------------------------------------------------------------------------------
# サブ辞書

    IMAGE_TABLE_COLUMNS = {
        "id": "INTEGER PRIMARY KEY AUTOINCREMENT",
        "name": "TEXT NOT NULL",
        "imageData": "BLOB NOT NULL",
        "createTime": "TEXT NOT NULL",
        "url": "TEXT NOT NULL",
        "title": "TEXT",
        "placement": "INTEGER CHECK (placement IN (1, 2, 3, 4))",
        "priority": "INTEGER NOT NULL",
        "status": "TEXT CHECK (status IN ('complete', 'Error'))",
    }


# ----------------------------------------------------------------------------------
#* メイン辞書

    TABLE_PATTERN = {
        "cookiesDB": COOKIES_TABLE_COLUMNS,
        "text": TEXT_TABLE_COLUMNS,
        "image": IMAGE_TABLE_COLUMNS
    }


# ----------------------------------------------------------------------------------


class TableName:
    TEXT_TABLE_COLUMNS="TEXT_TABLE_COLUMNS"