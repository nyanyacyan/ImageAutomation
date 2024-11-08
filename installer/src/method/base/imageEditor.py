# coding: utf-8
# $$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$

# $$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$
# import
import os, requests
from selenium.webdriver.chrome.webdriver import WebDriver
from PIL import Image, ImageDraw, ImageFont
from typing import Tuple, List
from io import BytesIO



# 自作モジュール
from utils import Logger
from installer.src.method.constElementPath import ImageInfo


# $$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$
# **********************************************************************************


class ImageEditor:
    def __init__(self, debugMode=True):
        # logger
        self.getLogger = Logger(__name__, debugMode=debugMode)
        self.logger = self.getLogger.getLogger()

        self.imageSize = (1080, 1080)


# ----------------------------------------------------------------------------------


    def executePatternEditors(self, data: dict):
        patterns = ['A', 'B', 'C', 'D']
        pattern_classes = {
            'A': PatternAEditor,
            'B': PatternBEditor,
            'C': PatternCEditor,
            'D': PatternDEditor
        }

        for pattern in patterns:
            if pattern not in data:
                self.logger.error(f"{pattern} パターンのデータが欠けているため、{pattern} とそれ以降のすべてのパターンをスキップします。")
                break

            # パターン固有のデータを取得
            pattern_data = data[pattern]  # 各パターンのリストのみを取得
            baseImagePath = ImageInfo.BASE_IMAGE_PATH.value[pattern]
            fontSize = ImageInfo.FONT_SIZES.value[pattern]
            fontPath = ImageInfo.FONT_PATH.value
            outputFolder = ImageInfo.OUTPUT_PATH.value

            # クラスのインスタンスを作成して処理を開始
            editor_class = pattern_classes[pattern]
            editor = editor_class()

            # デバッグログを追加
            self.logger.info(f"executePatternEditors 呼び出し時の {pattern} のデータの内容: {pattern_data}")

            # 画像作成メソッドにパターン固有の情報を渡す
            if not editor.createImage(pattern_data, fontPath, baseImagePath, fontSize, outputFolder, pattern):
                self.logger.error(f"パターン {pattern} の画像データが揃ってないため、以降のパターンをスキップします。")
                break

        self.logger.info(f"画像処理が完了しました。")



# ----------------------------------------------------------------------------------
# 画像が揃っているかチェック

    def checkImageUrl(self, data: list, pattern: str):
        # 各項目が辞書であることを確認してからアクセスする
        for item in data:
            if pattern == 'A' and 'imagePath' not in item:
                continue

            if not isinstance(item, dict):
                self.logger.error(f"{pattern} のデータ形式が不正です。辞書形式が期待されますが、{type(item)} が見つかりました。")
                return False

            if 'imagePath' not in item:
                self.logger.error(f"{pattern} のデータに 'imagePath' キーが見つかりません。データ: {item}")
                return False

            try:
                response = requests.head(item['imagePath'], allow_redirects=True)
                if response.status_code < 200 or response.status_code >= 400:
                    self.logger.error(f"{pattern} の画像が見つかりません: \n{item['imagePath']}")
                    return False
            except requests.RequestException as e:
                self.logger.error(f"{pattern} の画像データにアクセスできません。: \n{item['imagePath']}\nエラー: {e}")
                return False

        return True



# ----------------------------------------------------------------------------------


    def checkImageCount(self, data: List, imageNum: int, pattern: str):
        if len(data) < imageNum:
            self.logger.error(f"{pattern} に必要な画像枚数が不足しています。\n必要: {self.imageNum}\n実際: {len(data)}")
            return False
        return True


# ----------------------------------------------------------------------------------
# 抽象メソッド（実装がないメソッド）
# 画像編集の具体的な処理を記述するためのメソッド
# 具体的に何をどう編集するかはわからないため、編集の詳細な実装は行わず、空のメソッドとして定義
# raise NotImplementedError の部分は、もしサブクラスでこのメソッドが実装されていなければエラーを発生させ、「実装が必要です」と警告する役割
#? baseImage: 編集する画像本体
#? draw: 画像上にテキストや図形を描くためのツール
#? font: テキストのフォント
#? width, height: 画像の幅と高さ
# NotImplementedError の意図はeditImage が基底クラス内で使われる場面で、サブクラスがこのメソッドをオーバーライドしていないとエラーが発生します。これにより、サブクラスにこのメソッドの実装を忘れないように促してる

    def editImage(
        self,
        data: list,
        baseImage: Image.Image,
        draw: ImageDraw.ImageDraw,
        font: ImageFont.FreeTypeFont,
        pattern: str,
        width: int,
        height: int
    ):
        raise NotImplementedError("サブクラスにてこのメソッドを実装する必要があります。")


# ----------------------------------------------------------------------------------


    def createImage(self, data: list, fontPath: str, baseImagePath: str, fontSize: int, outputFolder: str, pattern: str):
        '''
        fontPath→使用したいフォントを指定する
        baseImagePath→ベース画像を指定する
        '''
        self.logger.info(f"createImage 呼び出し時の {pattern} の data の型: {type(data)}")
        self.logger.info(f"createImage 呼び出し時の {pattern} の data の内容: {data}")

        if not self.checkImageCount(data, len(data), pattern):
            return False
        if not self.checkImageUrl(data, pattern):
            return False

        # ベース画像の読み込み
        print(f"baseImagePath: {baseImagePath}")
        baseImage = Image.open(baseImagePath).resize(self.imageSize).convert("RGBA")
        width, height = baseImage.size
        draw = ImageDraw.Draw(baseImage)
        font = ImageFont.truetype(fontPath, fontSize)

        # サブクラスで実装されたeditImageメソッドを呼び出し
        self.editImage(data, baseImage, draw, font, pattern, width, height)

        outputFilePath = os.path.join(outputFolder, f"output_{pattern}.png")
        baseImage.save(outputFilePath, format="PNG")
        self.logger.info(f"保存完了: {outputFilePath}")

        return True


# ----------------------------------------------------------------------------------


    def drawTextWithWrapping(
        self,
        draw: ImageDraw.ImageDraw,
        text: str,
        font: ImageFont.FreeTypeFont,
        maxWidth: int,
        startPosition: Tuple[str, str],  # 式を表す文字列として受け取る
        lineHeight: int,
        fill: Tuple[int, int, int] = (0, 0, 0),
        mode: str = "wrap"
    ):

        # startPosition の各要素を確認し、文字列の場合は eval() で評価し、intに直して計算する
        if isinstance(startPosition[0], str):
            try:
                self.logger.debug(f"startPosition[0]が文字列だったの計算してint変換")
                x = eval(startPosition[0], {"width": maxWidth, "height": lineHeight})
            except Exception as e:
                self.logger.error(f"startPosition[0] の評価に失敗しました: {startPosition[0]}\nエラー: {e}")
                return
        else:
            x = startPosition[0]

        if isinstance(startPosition[1], str):
            try:
                self.logger.debug(f"startPosition[0]が文字列だったの計算してint変換")
                y = eval(startPosition[1], {"width": maxWidth, "height": lineHeight})
            except Exception as e:
                self.logger.error(f"startPosition[1] の評価に失敗しました: {startPosition[1]}\nエラー: {e}")
                return
        else:
            y = startPosition[1]

        self.logger.debug(f"\nx: {x}\ny: {y}")
        self.logger.debug(f"\nx: {type(x)}\ny: {type(y)}")

        lines = []

        if mode == "center":
            self.logger.info(f"textを中央に合わせて配置(改行で区切る): {text}")
            # 手動改行に基づいて行を分割し、各行を中央揃え
            lines = text.split('\n')
            for line in lines:
                lineWidth = draw.textlength(line, font=font)
                centered_x = x + (maxWidth - lineWidth) // 2
                draw.text((centered_x, y), line, font=font, fill=fill)
                y += lineHeight

        elif mode == "wrap":
            self.logger.info(f"文字を埋めていく(区切りなし): {text}")

            line = ""
            # テキストを1文字ずつ追加し、最大幅を超えたら改行
            for char in text:
                # 現在の行に文字を追加して幅をチェック
                if draw.textlength(line + char, font=font) <= maxWidth:
                    line += char
                else:
                    # 最大幅を超えた場合、行を確定して次の行に移る
                    lines.append(line)
                    line = char  # 次の行の最初の文字として設定
            lines.append(line)

            # 各行を指定の位置に描画
            for line in lines:
                draw.text((x, y), line, font=font, fill=fill)
                y += lineHeight




# ----------------------------------------------------------------------------------


    def drawImageWithMode(
            self,
            baseImage: Image.Image,
            imagePath: str,
            maxWidth: int,
            maxHeight: int,
            startPosition: Tuple[str, str],  # 式を表す文字列として受け取る
            mode: str = "wrap"
    ):
        # 画像を取得して `insertImage` を定義する
        if imagePath.startswith("http://") or imagePath.startswith("https://"):
            try:
                response = requests.get(imagePath, stream=True)
                response.raise_for_status()
                insertImage = Image.open(BytesIO(response.content)).convert("RGBA")
            except requests.RequestException as e:
                self.logger.error(f"画像の取得に失敗しました: {imagePath}\nエラー: {e}")
                return
        else:
            try:
                insertImage = Image.open(imagePath).convert("RGBA")
            except FileNotFoundError:
                self.logger.error(f"ローカル画像ファイルが見つかりません: {imagePath}")
                return

        print(f"startPosition: {startPosition}")

        # startPosition の各要素を確認し、文字列の場合は eval() で評価し、intに直して計算する
        if isinstance(startPosition[0], str):
            try:
                self.logger.debug(f"startPosition[0]が文字列だったの計算してint変換")
                x = eval(startPosition[0], {"width": baseImage.width, "height": baseImage.height})
            except Exception as e:
                self.logger.error(f"startPosition[0] の評価に失敗しました: {startPosition[0]}\nエラー: {e}")
                return
        else:
            x = startPosition[0]

        if isinstance(startPosition[1], str):
            try:
                self.logger.debug(f"startPosition[0]が文字列だったの計算してint変換")
                y = eval(startPosition[1], {"width": baseImage.width, "height": baseImage.height})
            except Exception as e:
                self.logger.error(f"startPosition[1] の評価に失敗しました: {startPosition[1]}\nエラー: {e}")
                return
        else:
            y = startPosition[1]

        self.logger.debug(f"\nx: {x}\ny: {y}")
        self.logger.debug(f"\nx: {type(x)}\ny: {type(y)}")


        # 画像の貼り付け
        baseImage.paste(insertImage, (x, y), insertImage)


# ----------------------------------------------------------------------------------
# 入れ込むデータ形式

# data = {
#     'A': [
#         {'image_path': 'path/to/imageA1.png', 'text': 'テキストA1'},  # 1つ目の画像とテキスト
#         {'text': 'テキストA2'},  # 2つ目のテキスト
#         {'text': 'テキストA3'}   # 3つ目のテキスト
#     ],
#     'B': [
#         {'image_path': 'path/to/imageB1.png', 'text': 'テキストB1'},
#         {'image_path': 'path/to/imageB2.png', 'text': 'テキストB2'}
#     ],
#     'C': [
#         {'image_path': 'path/to/imageC1.png', 'text': 'テキストC1'},
#         {'image_path': 'path/to/imageC2.png', 'text': 'テキストC2'}
#     ],
#     'D': [
#         {'image_path': 'path/to/imageD1.png', 'text': 'テキストD1'},
#         {'image_path': 'path/to/imageD2.png', 'text': 'テキストD2'}
#     ]
# }

# **********************************************************************************


class PatternAEditor(ImageEditor):
    def editImage(self, data: List, baseImage, draw, font, pattern: str, baseWidth, baseHeight):
        '''
        親クラスにはなにも定義されてないのでオーバーライドの最後の部分は不要
        imagePath→は後で入れ込むdataのkeyによって変更書ける
        .resize(self.image_size)は画像のサイズを編集
        Image.open(data[0]['imagePath'])→画像を呼び出している
        .convert("RGBA")画像の色を変更するための準備

        draw.textは画像に文字を挿入する命令
        画像の縦の真ん中あたり (height // 2) に文字を配置
        fillは文字の色の設定 (255, 255, 255)=白、(0, 0, 0)=黒
        baseWidthとbaseHeightはこれから使う際のためのもの
        '''
        maxWidth = ImageInfo.MAX_WIDTH.value
        lineHeight = ImageInfo.LINE_HEIGHT.value
        fillColor = ImageInfo.FILL_COLOR_BLACK.value

        # START_POSITIONS を使用して位置を取得
        startPositions = ImageInfo.START_POSITIONS.value[pattern]

        # startPositions['IMAGE_CENTER'] がタプル形式か確認
        if not isinstance(startPositions['IMAGE_CENTER'], (tuple, list)) or len(startPositions['IMAGE_CENTER']) != 2:
            self.logger.error(f"startPositions['IMAGE_CENTER'] の形式が正しくありません: {startPositions['IMAGE_CENTER']}")
            return

        # 画像の配置
        self.drawImageWithMode(
            baseImage=baseImage,
            imagePath=data[0]['imagePath'],
            maxWidth=ImageInfo.IMAGE_SIZE.value[0],
            maxHeight=ImageInfo.IMAGE_SIZE.value[1],
            startPosition=startPositions['IMAGE_CENTER']
        )

        # テキストを左側、下側、右側に配置
        positions = ['TEXT_LEFT', 'TEXT_BOTTOM', 'TEXT_RIGHT']
        for i, pos in enumerate(positions):
            if not isinstance(startPositions[pos], (tuple, list)) or len(startPositions[pos]) != 2:
                self.logger.error(f"{pos} の位置が不正です: {startPositions[pos]}")
                continue

            if 'text' not in data[i]:
                self.logger.error(f"data[{i}] に 'text' キーがありません: {data[i]}")
                continue

            self.drawTextWithWrapping(
                draw=draw,
                text=data[i]['text'],
                font=font,
                maxWidth=maxWidth,
                startPosition=startPositions[pos],
                lineHeight=lineHeight,
                fill=fillColor,
                mode="wrap"
            )



# **********************************************************************************


class PatternBEditor(ImageEditor):
    def editImage(self, data: List, baseImage, draw, font, pattern: str, baseWidth, baseHeight):
        # 画像の配置
        maxWidth = ImageInfo.MAX_WIDTH.value
        lineHeight = ImageInfo.LINE_HEIGHT.value
        fillColor = ImageInfo.FILL_COLOR_BLACK.value

        # START_POSITIONS を使用して位置を取得
        startPositions = ImageInfo.START_POSITIONS.value[pattern]

        # 画像を2枚配置
        self.drawImageWithMode(
            baseImage=baseImage,
            imagePath=data[0]['imagePath'],
            maxWidth=ImageInfo.IMAGE_SIZE_SMALL.value[0],
            maxHeight=ImageInfo.IMAGE_SIZE_SMALL.value[1],
            startPosition=startPositions['IMAGE_TOP_LEFT'],
            mode="wrap"
        )

        self.drawImageWithMode(
            baseImage=baseImage,
            imagePath=data[1]['imagePath'],
            maxWidth=ImageInfo.IMAGE_SIZE_SMALL.value[0],
            maxHeight=ImageInfo.IMAGE_SIZE_SMALL.value[1],
            startPosition=startPositions['IMAGE_BOTTOM_LEFT'],
            mode="wrap"
        )

        # テキストを右上と右下に配置
        self.drawTextWithWrapping(
            draw=draw,
            text=data[0]['text'],
            font=font,
            maxWidth=maxWidth,
            startPosition=startPositions['TEXT_TOP_RIGHT'],
            lineHeight=lineHeight,
            fill=fillColor,
            mode="wrap"
        )

        self.drawTextWithWrapping(
            draw=draw,
            text=data[1]['text'],
            font=font,
            maxWidth=maxWidth,
            startPosition=startPositions['TEXT_BOTTOM_RIGHT'],
            lineHeight=lineHeight,
            fill=fillColor,
            mode="wrap"
        )


# **********************************************************************************


class PatternCEditor(ImageEditor):
    def editImage(self, data: List, baseImage, draw, font, pattern: str, baseWidth, baseHeight):
        # 画像の配置
        maxWidth = ImageInfo.MAX_WIDTH.value
        lineHeight = ImageInfo.LINE_HEIGHT.value
        fillColor = ImageInfo.FILL_COLOR_BLACK.value

        # START_POSITIONS を使用して位置を取得
        startPositions = ImageInfo.START_POSITIONS.value[pattern]

        # 画像を2枚配置
        self.drawImageWithMode(
            baseImage=baseImage,
            imagePath=data[0]['imagePath'],
            maxWidth=ImageInfo.IMAGE_SIZE_SMALL.value[0],
            maxHeight=ImageInfo.IMAGE_SIZE_SMALL.value[1],
            startPosition=startPositions['IMAGE_TOP_LEFT'],
            mode="wrap"
        )

        self.drawImageWithMode(
            baseImage=baseImage,
            imagePath=data[1]['imagePath'],
            maxWidth=ImageInfo.IMAGE_SIZE_SMALL.value[0],
            maxHeight=ImageInfo.IMAGE_SIZE_SMALL.value[1],
            startPosition=startPositions['IMAGE_BOTTOM_LEFT'],
            mode="wrap"
        )

        # テキストを右上と右下に配置
        self.drawTextWithWrapping(
            draw=draw,
            text=data[0]['text'],
            font=font,
            maxWidth=maxWidth,
            startPosition=startPositions['TEXT_TOP_RIGHT'],
            lineHeight=lineHeight,
            fill=fillColor,
            mode="wrap"
        )

        self.drawTextWithWrapping(
            draw=draw,
            text=data[1]['text'],
            font=font,
            maxWidth=maxWidth,
            startPosition=startPositions['TEXT_BOTTOM_RIGHT'],
            lineHeight=lineHeight,
            fill=fillColor,
            mode="wrap"
        )

# **********************************************************************************


class PatternDEditor(ImageEditor):
    def editImage(self, data: List, baseImage, draw, font, pattern: str, baseWidth, baseHeight):
        # 画像の配置
        maxWidth = ImageInfo.MAX_WIDTH.value
        lineHeight = ImageInfo.LINE_HEIGHT.value
        fillColor = ImageInfo.FILL_COLOR_BLACK.value

        # START_POSITIONS を使用して位置を取得
        startPositions = ImageInfo.START_POSITIONS.value[pattern]

        # 画像を2枚配置
        self.drawImageWithMode(
            baseImage=baseImage,
            imagePath=data[0]['imagePath'],
            maxWidth=ImageInfo.IMAGE_SIZE_SMALL.value[0],
            maxHeight=ImageInfo.IMAGE_SIZE_SMALL.value[1],
            startPosition=startPositions['IMAGE_TOP_LEFT'],
            mode="wrap"
        )

        self.drawImageWithMode(
            baseImage=baseImage,
            imagePath=data[1]['imagePath'],
            maxWidth=ImageInfo.IMAGE_SIZE_SMALL.value[0],
            maxHeight=ImageInfo.IMAGE_SIZE_SMALL.value[1],
            startPosition=startPositions['IMAGE_BOTTOM_LEFT'],
            mode="wrap"
        )

        # テキストを右上と右下に配置
        self.drawTextWithWrapping(
            draw=draw,
            text=data[0]['text'],
            font=font,
            maxWidth=maxWidth,
            startPosition=startPositions['TEXT_TOP_RIGHT'],
            lineHeight=lineHeight,
            fill=fillColor,
            mode="wrap"
        )

        self.drawTextWithWrapping(
            draw=draw,
            text=data[1]['text'],
            font=font,
            maxWidth=maxWidth,
            startPosition=startPositions['TEXT_BOTTOM_RIGHT'],
            lineHeight=lineHeight,
            fill=fillColor,
            mode="wrap"
        )

# **********************************************************************************


data = {
    'A': [
        {'imagePath': 'https://property.es-img.jp/rent/img/100000000000000000000008972046/0100000000000000000000008972046_10.jpg?iid=3090815223', 'text': '京王線'},  # 1つ目の画像とテキスト
        {'text': '徒歩3分'},  # 2つ目のテキスト
        {'text': '調布駅'}   # 3つ目のテキスト
    ],
    'B': [
        {'imagePath': 'https://property.es-img.jp/rent/img/100000000000000000000008972046/0100000000000000000000008972046_1.jpg?iid=1876367453', 'text': 'テキストB1'},
        {'imagePath': 'https://property.es-img.jp/rent/img/100000000000000000000008972046/0100000000000000000000008972046_6.jpg?iid=2654214310', 'text': 'テキストB2'}
    ],
    'C': [
        {'imagePath': 'https://property.es-img.jp/rent/img/100000000000000000000008972046/0100000000000000000000008972046_14.jpg?iid=3042973924', 'text': 'テキストC1'},
        {'imagePath': 'https://property.es-img.jp/rent/img/100000000000000000000008972046/0100000000000000000000008972046_19.jpg?iid=2286688419', 'text': 'テキストC2'}
    ],
    'D': [
        {'imagePath': 'https://property.es-img.jp/rent/img/100000000000000000000008972046/0100000000000000000000008972046_5.jpg?iid=1835735112', 'text': 'テキストD1'},
        {'imagePath': 'https://property.es-img.jp/rent/img/100000000000000000000008972046/0100000000000000000000008972046_4.jpg?iid=2240682102', 'text': 'テキストD2'}
    ]
}



# Instantiate the main ImageEditor class and execute pattern editors
if __name__ == "__main__":
    image_editor = ImageEditor(debugMode=True)
    image_editor.executePatternEditors(data)
