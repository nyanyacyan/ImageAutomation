# coding: utf-8
# $$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$
# Pathの設定 export PYTHONPATH="${PYTHONPATH}:/Users/nyanyacyan/Desktop/project_file/SNS_auto_upper/installer/src/method/base"

# $$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$
# import

import pytest, time
from unittest.mock import patch, AsyncMock, MagicMock, PropertyMock

# 自作モジュール
from installer.src.method.base.cookieManager import CookieManager


# $$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$
# **********************************************************************************
# 単体テスト 写真を取得

class TestCookie:

# ----------------------------------------------------------------------------------


    def testCookieSuccess(self):
        chrome = MagicMock()
        homeUrl = 'http://example.com'

        instance = CookieManager(chrome=chrome, homeUrl=homeUrl, debugMode=True)

        with patch.object(instance.__class__, 'getCookies', new_callable=PropertyMock) as mock_getCookie:
            mock_getCookie.return_value = [{
                'Name': "sessionId",
                'Value': "dummySession",
                'domain': "example.com",
                'path': "/",
                'expires': int(time.time()) + 3600,
                'max-age': 3600
            }]


            result = instance.checkCookieInDB()

            assert result == mock_getCookie.return_value

# ----------------------------------------------------------------------------------