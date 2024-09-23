#  coding: utf-8
# 文字列をすべてここに保管する
# ----------------------------------------------------------------------------------
# 2024/7/17 更新

# ----------------------------------------------------------------------------------
from enum import Enum


# ----------------------------------------------------------------------------------
# DiscordUrl

class Debug(Enum):
    discord = 'https://discord.com/api/webhooks/1220239805204660314/niMRY1OVJwYh3PY9X9EfF2O6C7ZPhukRDoXfsXlwGBz4n1HKE81MA1B6TQiy2FUnzHfk'

# ----------------------------------------------------------------------------------
# エラーメッセージ

class ErrorMessage(Enum):
    ApiRequestError='上限までリクエストをしましたがエラー'

# ----------------------------------------------------------------------------------
# 通知メッセージ



# ----------------------------------------------------------------------------------
# アカウントID

class AccountId(Enum):
    pass


# ----------------------------------------------------------------------------------
# 各Fileの名称

class FileName(Enum):
    pass


# ----------------------------------------------------------------------------------
# GCPのjsonファイルなどのKeyFile

class KeyFile(Enum):
    gssKeyFile='sns-auto-430920-08274ad68b41.json'


# ----------------------------------------------------------------------------------
# スプシID

class GssSheetId(Enum):
    XSheetId='1HQQXFCPktJjlY-MfJvudQos2ljbIvhY4spR3CfEYziw'
    InstagramSheetId=''


# ----------------------------------------------------------------------------------
# スプシのColumn

class GssColumns(Enum):
    conditionCol='条件'
    testimonialsCol='体験談'
    keywordCol='キーワード'
    hashtagCol='ハッシュタグ'
    exampleCol='例文'
    beforeCol='前回の文章'
    photoColName='画像'


# ----------------------------------------------------------------------------------
# サイトURL

class SiteUrl(Enum):
    #* スプシの最後をCSV出力に変更する→これによりDFにすることができる
    # https://docs.google.com/spreadsheets/d/[spreadsheetId]/export?format=csv
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
    X='X(twitter)'
    Instagram='Instagram'



# ----------------------------------------------------------------------------------


class xUtils(Enum):
    maxlen=280



# ----------------------------------------------------------------------------------
# XのPromptFormat
# ハッシュタグは文字数に含まれる（最大280文字）

class XPromptFormat(Enum):
    openingComment='これから「X（旧Twitter）」に投稿する文章の生成をお願いします。\n下記にある①〜⑥の「条件」「体験談」「キーワード」「ハッシュタグ」「例」「前回の文章」を参考に文章の生成をしてください。'


    conditionFormat='①文章を作成の際の条件:\n{list}'


    testimonialsFormat='②下記の発信したい体験談の内容:\n{list}'


    keywordFormat='③下記のキーワードの中から2つ入れて文章を作成してください:\n{list}'

    # 最大の文字数に収まる様にする
    hashtagFormat='④下記のハッシュタグを必ず文章の中の最後に入れてください:\n{list}'


    exampleFormat='⑤下記の文章を参考に作成してください:\n{list}'


    beforeFormat='⑥下記の文章は前回の文章です。前回の内容とは別の内容の文章にしてください:\n{list}'


    endingComment='上記の①〜⑥までの事柄を必ず守って作成をお願い致します。'


    fixedPrompt='文字数をオーバーしております。「投稿に必要な文章のみ」responseしてください。'

    notifyMsg='下記のメッセージを確認の上、フォーマットにて返信をお願い致します。\n\n今回の文章でようでしょうか？\nOK or NG\n\n修正が必要な場合にはどのような文章が良いでしょうか？\n修正指示:\n\nSNSの種類は\nX'


# ----------------------------------------------------------------------------------
# InstagramPromptFormat
# ハッシュタグは文字数に含まれる（最大2200文字）
# ハッシュタグは最大30個まで

class InstagramPromptFormat(Enum):
    openingComment='これから「Instagram」に投稿する文章の生成をお願いします。\n下記にある「条件」「体験談」「キーワード」「例」「前回の文章」を参考に文章の生成をしてください。'


    conditionFormat='①文章を作成する上で必ず守っとほしい条件は以下の通りです:\n{list}'


    testimonialsFormat='②下記の体験談から発信すべき内容を抜き出してください:\n{list}'


    keywordFormat='③下記のキーワードの中から2つ入れて文章を作成してください:\n{list}'

    # 最大の文字数に収まる様にする
    hashtagFormat='④下記のハッシュタグを必ず文章の中の最後に入れてください:\n{list}'


    exampleFormat='⑤下記の文章を参考に作成してください:\n{list}'


    beforeFormat='⑥下記の文章は前回の文章です。前回の内容とは別の内容の文章にしてください:\n{list}'


    endingComment='上記の①〜⑥までの事柄を必ず守って作成をお願い致します。'


    againComment='文字数をオーバーしております。「投稿に必要な文章のみ」responseしてください。'


# ----------------------------------------------------------------------------------
# # ChatgptUtils

class ChatgptUtils(Enum):
    # "gpt-4o-mini-2024-07-18" or "gpt-4o-2024-08-06"
    model='gpt-4o-mini-2024-07-18'

    endpointUrl='https://api.openai.com/v1/chat/completions'

    MaxToken=16000

# ----------------------------------------------------------------------------------
