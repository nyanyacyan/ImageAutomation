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

    TEXT_TABLE_COLUMNS = {
        "id": "INTEGER PRIMARY KEY AUTOINCREMENT",
        "name": "TEXT NOT NULL",
        "getWord": "TEXT NOT NULL",
        "createTime": "INTEGER NOT NULL",
        "url": "TEXT",
        "title": "TEXT",
        "status": "TEXT CHECK (status IN ('complete', 'Error', NULL))"
    }


# ----------------------------------------------------------------------------------
# サブ辞書

    IMAGE_TABLE_COLUMNS = {
        "id": "INTEGER PRIMARY KEY AUTOINCREMENT",
        "name": "TEXT NOT NULL",
        "imageData": "BLOB NOT NULL",
        "createTime": "INTEGER NOT NULL",
        "url": "TEXT",
        "title": "TEXT",
        "status": "TEXT CHECK (status IN ('complete', 'Error', NULL))"
    }


# ----------------------------------------------------------------------------------
#* メイン辞書

    TABLE_PATTERN = {
        "cookiesDB": COOKIES_TABLE_COLUMNS,
        "text": TEXT_TABLE_COLUMNS,
        "image": IMAGE_TABLE_COLUMNS
    }


# ----------------------------------------------------------------------------------
