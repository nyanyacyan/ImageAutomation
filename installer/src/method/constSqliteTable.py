# coding: utf-8
# $$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$

# $$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$
# import


# $$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$
# **********************************************************************************
# サブ辞書

COOKIES_TABLE_COLUMNS = {
    "id": "PRIMARY KEY AUTOINCREMENT",
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
    "startWord": "TEXT NOT NULL"
}


# ----------------------------------------------------------------------------------
# サブ辞書

IMAGE_TABLE_COLUMNS = {
    "startImage": "BLOB NOT NULL"
}


# ----------------------------------------------------------------------------------
#* メイン辞書

TABLE_PATTERN = {
    "cookies": COOKIES_TABLE_COLUMNS,
    "text": TEXT_TABLE_COLUMNS,
    "image": IMAGE_TABLE_COLUMNS
}


# ----------------------------------------------------------------------------------
