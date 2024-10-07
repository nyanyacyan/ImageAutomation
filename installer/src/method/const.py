#  coding: utf-8
# 文字列をすべてここに保管する
# ----------------------------------------------------------------------------------
# 2024/7/17 更新

# ----------------------------------------------------------------------------------
from enum import Enum


# ----------------------------------------------------------------------------------
# サイトURL

class SiteUrl(Enum):
    LoginUrl=''
    HomeUrl=''
    TargetUrl=''


# ----------------------------------------------------------------------------------


class LoginInfo(Enum):
    IDLoginInfo={
        'idBy': '',
        'idValue': '',
        'idText': '',
        'passBy': '',
        'passValue': '',
        'passText': '',
        'btnBy': '',
        'btnValue': '',
        'btnText': ''
    }


# ----------------------------------------------------------------------------------


class Dir(Enum):
    result='resultOutput'
    input='inputData'


# ----------------------------------------------------------------------------------


class SubDir(Enum):
    pickles='pickles'
    cookies='cookies'
    DBSubDir='DB'


# ----------------------------------------------------------------------------------


class TableName(Enum):
    Cookie='cookiesDB'


# ----------------------------------------------------------------------------------


class ColumnsName(Enum):
    Cookies=('name', 'value', 'domain', 'path', 'expires', 'maxAge', 'createTime')

    PRIMARY_KEY='id'

# ----------------------------------------------------------------------------------


class Extension(Enum):
    text='.txt'
    csv='.csv'
    json='.json'
    pickle='.pkl'
    excel='.xlsx'
    yaml='.yaml'
    cookie='cookie.pkl'
    DB='.db'


# ----------------------------------------------------------------------------------


class Encoding(Enum):
    utf8='utf-8'


# ----------------------------------------------------------------------------------
# DiscordUrl

class Debug(Enum):
    discord = 'https://discord.com/api/webhooks/1220239805204660314/niMRY1OVJwYh3PY9X9EfF2O6C7ZPhukRDoXfsXlwGBz4n1HKE81MA1B6TQiy2FUnzHfk'


# ----------------------------------------------------------------------------------
# エラーメッセージ

class ErrorMessage(Enum):
    ApiRequestError='上限までリクエストをしましたがエラー'
    chromeDriverManagerError='PCの再起動で\n改善する可能性があります。PCの再起動をされますか？'
    chromeDriverManagerErrorTitle='Chromeが正しくinstallできませんでした。'


# ----------------------------------------------------------------------------------
# 通知メッセージ



# ----------------------------------------------------------------------------------
# アカウントID

class AccountId(Enum):
    pass


# ----------------------------------------------------------------------------------
# 各Fileの名称

class FileName(Enum):
    chromeOpIFrame='uBlock-Origin.crx'
    chromeOpCaptcha='hlifkpholllijblknnmbfagnkjneagid.crx'


# ----------------------------------------------------------------------------------
# GCPのjsonファイルなどのKeyFile

class KeyFile(Enum):
    gssKeyFile='sns-auto-430920-08274ad68b41.json'


# ----------------------------------------------------------------------------------
# スプシID

class GssSheetId(Enum):
    XSheetId=''
    InstagramSheetId=''


# ----------------------------------------------------------------------------------
# スプシのColumn

class GssColumns(Enum):
    pass


# ----------------------------------------------------------------------------------
# Endpoint

class EndPoint(Enum):
    Line ="https://notify-api.line.me/api/notify"
    Chatwork = 'https://api.chatwork.com/v2'
    Slack = 'https://slack.com/api/chat.postMessage'
    Discord = 'https://discord.com/api/webhooks/1220239805204660314/niMRY1OVJwYh3PY9X9EfF2O6C7ZPhukRDoXfsXlwGBz4n1HKE81MA1B6TQiy2FUnzHfk'

    ChatGPT = 'https://api.openai.com/v1/engines/{}/completions'
    X_image = 'https://upload.twitter.com/1.1/media/upload.json'
    X = 'https://api.twitter.com/2/tweets'

    Instagram = 'https://graph.facebook.com/v16.0/{}/media'
    InstagramImage = 'https://graph.facebook.com/v16.0/{}/media_publish'


# ----------------------------------------------------------------------------------


class SnsKinds(Enum):
    pass



# ----------------------------------------------------------------------------------
# ChatgptUtils

class ChatgptUtils(Enum):
    # "gpt-4o-mini-2024-07-18" or "gpt-4o-2024-08-06"
    model='gpt-4o-mini-2024-07-18'

    endpointUrl='https://api.openai.com/v1/chat/completions'

    MaxToken=16000

# ----------------------------------------------------------------------------------


