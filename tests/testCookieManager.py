# coding: utf-8
# $$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$
# Pathの設定 export PYTHONPATH="${PYTHONPATH}:/Users/nyanyacyan/Desktop/project_file/SNS_auto_upper/installer/src/method/base"

# $$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$
# import

import pytest, time
from unittest.mock import patch, AsyncMock

# 自作モジュール
from installer.src.method.base.cookieManager import CookieManager


# $$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$
# **********************************************************************************
# 単体テスト 写真を取得

class TestChrome:

# ----------------------------------------------------------------------------------


    def testCookie(self):
        instance = CookieManager(debugMode=True)

        with patch.object(instance, 'getCookies') as mock_getCookie:
            mock_getCookie.return_value = [{
                'Name': "sessionId",
                'Value': "dummySession",
                'domain': "example.com",
                'path': "/",
                'expires': int(time.time()) + 3600,
                'max-age': 3600
            }]


            instance.createCookieDB()

            instance.createCookieFile()

            instance.checkCookieLimit()

# ----------------------------------------------------------------------------------