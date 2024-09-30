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
# テストOK

    def testCookieManAgeSuccess(self):
        chrome = MagicMock()
        homeUrl = 'http://example.com'

        instance = CookieManager(chrome=chrome, homeUrl=homeUrl, debugMode=True)

        with patch.object(instance.__class__, 'getCookies', new_callable=PropertyMock) as mock_getCookie:
            mock_getCookie.return_value = [{
                'name': "sessionId",
                'value': "dummySession",
                'domain': "example.com",
                'path': "/",
                'expires': int(time.time()) + 3600,
                'max-age': 3600
            }]


            result = instance.checkCookieInDB()
            resultWithoutId = {key: value for key, value in result.items() if key != 'id' and key != 'max-age'}

            mock_getCookie_value = mock_getCookie.return_value[0]
            mockWithoutMaxAge = {key: value for key, value in mock_getCookie_value.items() if key != 'max-age'}

            print(resultWithoutId)
            assert resultWithoutId == mockWithoutMaxAge


# ----------------------------------------------------------------------------------
# テストOK

    def testCookieExpiresSuccess(self):
        chrome = MagicMock()
        homeUrl = 'http://example.com'

        instance = CookieManager(chrome=chrome, homeUrl=homeUrl, debugMode=True)

        with patch.object(instance.__class__, 'getCookies', new_callable=PropertyMock) as mock_getCookie:
            mock_getCookie.return_value = [{
                'name': "sessionId",
                'value': "dummySession",
                'domain': "example.com",
                'path': "/",
                'expires': int(time.time()) + 3600,
            }]


            result = instance.checkCookieInDB()
            resultWithoutId = {key: value for key, value in result.items() if key != 'id' and key != 'max-age'}

            mock_getCookie_value = mock_getCookie.return_value[0]
            mockWithoutMaxAge = {key: value for key, value in mock_getCookie_value.items() if key != 'max-age'}

            print(resultWithoutId)
            assert resultWithoutId == mockWithoutMaxAge


# ----------------------------------------------------------------------------------


    def testCookieNoExpires(self):
        chrome = MagicMock()
        homeUrl = 'http://example.com'

        instance = CookieManager(chrome=chrome, homeUrl=homeUrl, debugMode=True)

        with patch.object(instance.__class__, 'getCookies', new_callable=PropertyMock) as mock_getCookie:
            mock_getCookie.return_value = [{
                'name': "sessionId",
                'value': "dummySession",
                'domain': "example.com",
                'path': "/",
                'expires': '',
                'max-age': ''
            }]


            result = instance.checkCookieInDB()
            resultWithoutId = {key: value for key, value in result.items() if key != 'id'}

            mock_getCookie_value = mock_getCookie.return_value[0]
            mockWithoutMaxAge = {key: value for key, value in mock_getCookie_value.items() if key != 'max-age' and key != 'expires'}

            print(resultWithoutId)
            print(mockWithoutMaxAge)
            assert resultWithoutId == mockWithoutMaxAge


# ----------------------------------------------------------------------------------