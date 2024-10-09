#  coding: utf-8
# 文字列をすべてここに保管する
# ----------------------------------------------------------------------------------
# 2024/7/17 更新

# ----------------------------------------------------------------------------------
from enum import Enum


# ----------------------------------------------------------------------------------
# サイトURL

class SiteUrl(Enum):
    LoginUrl='https://meiwa-chukai.es-b2b.com/signIn'
    HomeUrl='https://www.meiwakanzai.co.jp/'
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
# element

class Element(Enum):
    element


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


class ChatGptPrompt(Enum):
    prompt1=""


    prompt2=""


# ----------------------------------------------------------------------------------


class NGWordList(Enum):
    ngWords=[
        'バス有',
        'バストイレ同室',
        'トイレ有',
        'エアコン',
        '洗面所にドア',
        'ＢＳ',
        'ＣＳ',
        'ＣＡＴＶ',
        '電話回線',
        'ネット専用回線',
        '光ファイバー',
        'インターネット専用線配線済み',
        'インターホン',
        '収納有',
        '給湯',
        '冷房',
        '暖房',
        'フローリング',
        '室内洗濯機置場',
    ]

# ----------------------------------------------------------------------------------

class Address(Enum):
    addressList = [
    '北海道', '青森県', '岩手県', '宮城県', '秋田県', '山形県', '福島県',
    '茨城県', '栃木県', '群馬県', '埼玉県', '千葉県', '東京都', '神奈川県',
    '新潟県', '富山県', '石川県', '福井県', '山梨県', '長野県', '岐阜県',
    '静岡県', '愛知県', '三重県', '滋賀県', '京都府', '大阪府', '兵庫県',
    '奈良県', '和歌山県', '鳥取県', '島根県', '岡山県', '広島県', '山口県',
    '徳島県', '香川県', '愛媛県', '高知県', '福岡県', '佐賀県', '長崎県',
    '熊本県', '大分県', '宮崎県', '鹿児島県', '沖縄県'
]

# ----------------------------------------------------------------------------------
