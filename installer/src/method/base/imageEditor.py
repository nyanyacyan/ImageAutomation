# coding: utf-8
# $$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$

# $$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$
# import
import os, requests
from selenium.webdriver.chrome.webdriver import WebDriver
from PIL import Image, ImageDraw, ImageFont
from typing import Tuple


# 自作モジュール
from .utils import Logger
from installer.src.method.constElementPath import ImageInfo


# $$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$
# **********************************************************************************


class ImageEditor:
    def __init__(self, pattern: str, data: list, debugMode=True):
        # logger
        self.getLogger = Logger(__name__, debugMode=debugMode)
        self.logger = self.getLogger.getLogger()

        self.pattern = pattern
        self.data = data[pattern]

        self.baseImagePath = ImageInfo.IMAGE_PATH.value[{pattern}]
        self.fontSize = ImageInfo.FONT_SIZES.value[{pattern}]
        self.imageNum = ImageInfo.IMAGE_NUM.value[{pattern}]

        self.imageSize = (1080, 1080)


# ----------------------------------------------------------------------------------


    def execute_pattern_editors(self, data: dict, fontPath: str, outputFolder: str):
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

            editor_class = pattern_classes[pattern]
            editor = editor_class(pattern, data)
            if not editor.createImage(fontPath, outputFolder):
                self.logger.error(f"パターン {pattern} の画像データが揃ってないため、以降のパターンをスキップします。")
                break

        self.logger.info(f"画像処理が完了しました。")



# ----------------------------------------------------------------------------------
# 画像が揃っているかチェック

    def checkImageUrl(self):
        for item in self.data:
            try:
                # allow_redirects=Trueは短縮URLなどリダイレクトされてることがあること自動許可する
                response = requests.head(item['imagePath'], allow_redirects=True)
                if response.status_code < 200 or response.status_code >= 400:
                    self.logger.error(f"{self.pattern} の画像が見つかりません: \n{item['imagePath']}")
                    return False
            except requests.RequestException as e:
                self.logger.error(f"{self.pattern} の画像データにアクセスできません。: \n{item['imagePath']}\nエラー: {e}")
                return False

        return True


# ----------------------------------------------------------------------------------


    def checkImageCount(self):
        if len(self.data) < self.imageNum[self.pattern]:
            self.logger.error(f"{self.pattern} に必要な画像枚数が不足しています。\n必要: {self.imageNum}\n実際: {len(self.data)}")
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
            base_image: Image.Image,
            draw: ImageDraw.ImageDraw,
            font: ImageFont.FreeTypeFont,
            width: int,
            height: int
    ):

        raise NotImplementedError("サブクラスとして実装されてません。サブクラスにてこのメソッドを実装する必要があります。")


# ----------------------------------------------------------------------------------


    def createImage(self, fontPath: str, outputFolder: str):
        '''
        fontPath→使用したいフォントを指定する
        '''
        if not self.checkImageCount():
            return False
        if not self.checkImageUrl():
            return False

        baseImage = Image.open(self.baseImagePath).resize(self.imageSize).convert("RGBA")
        width, height = baseImage.size
        draw = ImageDraw.Draw(baseImage)
        font = ImageFont.truetype(fontPath, self.fontSize)

        self.editImage(baseImage, draw, font, width, height)

        outputFilePath = os.path.join(outputFolder, f"output_{self.pattern}.png")

        baseImage.save(outputFilePath, format="PNG")
        self.logger.info(f"保存完了: {outputFilePath}")
        return True


# ----------------------------------------------------------------------------------


    def drawTextWithWrapping(
        self,
        draw: ImageDraw.ImageDraw,
        text: str,
        font: str,
        maxWidth: int,
        startPosition: Tuple[int, int],
        lineHeight: int,
        fill: Tuple[int, int, int] = (0, 0, 0),
        mode: str = "wrap"
    ):

        x, y = startPosition
        lines = []

        if mode == "center":
            # 手動改行に基づいて行を分割し、各行を中央揃え
            lines = text.split('\n')
            for line in lines:
                lineWidth = draw.textsize(line, font=font)[0]
                centered_x = x + (maxWidth - lineWidth) // 2
                draw.text((centered_x, y), line, font=font, fill=fill)
                y += lineHeight


        elif mode == "wrap":
            # テキストを1文字ずつ追加し、最大幅を超えたら改行
            for char in text:
                # 現在の行に文字を追加して幅をチェック
                if draw.textsize(line + char, font=font)[0] <= maxWidth:
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
            startPosition: Tuple[int, int],
            mode: str = "wrap"
    ):

        if mode == "wrap":
            self.logger.info(f"指定した場所に配置: {startPosition}")

            insertImage = Image.open(imagePath).convert("RGBA")
            x, y = startPosition

        elif mode == "center":
            x = startPosition[0] + (maxWidth - insertImage.width) // 2
            y = startPosition[1] + (maxHeight - insertImage.height) // 2
            self.logger.info(f"指定した枠の中の中央に配置: {x}:{y}")

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
    def editImage(self, baseImage, draw, font, baseWidth, baseHeight):
        '''
        親クラスにはなにも定義されてないのでオーバーライドの最後の部分は不要
        imagePath→は後で入れ込むdataのkeyによって変更書ける
        .resize(self.image_size)は画像のサイズを編集
        Image.open(self.data[0]['imagePath'])→画像を呼び出している
        .convert("RGBA")画像の色を変更するための準備

        draw.textは画像に文字を挿入する命令
        画像の縦の真ん中あたり (height // 2) に文字を配置
        fillは文字の色の設定 (255, 255, 255)=白、(0, 0, 0)=黒
        baseWidthとbaseHeightはこれから使う際のためのもの
        '''
        # 画像の入れ込み
        # 1枚目の画像とtextの配置
        maxWidth = ImageInfo.MAX_WIDTH.value
        lineHeight = ImageInfo.LINE_HEIGHT.value
        fillColor = ImageInfo.FILL_COLOR_BLACK.value

        # START_POSITIONS を使用して位置を取得
        startPositions = ImageInfo.START_POSITIONS.value[self.pattern]

        # 画像の配置
        centerPosition = startPositions['IMAGE_CENTER']
        self.drawImageWithMode(
            baseImage=baseImage,
            imagePath=self.data[0]['imagePath'],
            maxWidth=ImageInfo.IMAGE_SIZE.value,
            maxHeight=centerPosition,
            startPosition=startPositions,
        )

        # テキストを左側、下側、右側に配置
        self.drawTextWithWrapping(
            draw=draw,
            text=self.data[0]['text'],
            font=font,
            maxWidth=maxWidth,
            startPosition=startPositions['TEXT_LEFT'],
            lineHeight=lineHeight,
            fill=fillColor,
            mode="wrap"
        )

        self.drawTextWithWrapping(
            draw=draw,
            text=self.data[1]['text'],
            font=font,
            maxWidth=maxWidth,
            startPosition=startPositions['TEXT_BOTTOM'],
            lineHeight=lineHeight,
            fill=fillColor,
            mode="wrap"
        )

        self.drawTextWithWrapping(
            draw=draw,
            text=self.data[2]['text'],
            font=font,
            maxWidth=maxWidth,
            startPosition=startPositions['TEXT_RIGHT'],
            lineHeight=lineHeight,
            fill=fillColor,
            mode="wrap"
        )


# **********************************************************************************


class PatternBEditor(ImageEditor):
    def editImage(self, baseImage, draw, font, baseWidth, baseHeight):
        # 画像の配置
        maxWidth = ImageInfo.MAX_WIDTH.value
        lineHeight = ImageInfo.LINE_HEIGHT.value
        fillColor = ImageInfo.FILL_COLOR_BLACK.value

        # START_POSITIONS を使用して位置を取得
        startPositions = ImageInfo.START_POSITIONS.value[self.pattern]

        # 画像を2枚配置
        self.drawImageWithMode(
            baseImage=baseImage,
            imagePath=self.data[0]['imagePath'],
            maxWidth=ImageInfo.IMAGE_SIZE_SMALL.value[0],
            maxHeight=ImageInfo.IMAGE_SIZE_SMALL.value[1],
            startPosition=startPositions['IMAGE_TOP_LEFT'],
            mode="wrap"
        )

        self.drawImageWithMode(
            baseImage=baseImage,
            imagePath=self.data[1]['imagePath'],
            maxWidth=ImageInfo.IMAGE_SIZE_SMALL.value[0],
            maxHeight=ImageInfo.IMAGE_SIZE_SMALL.value[1],
            startPosition=startPositions['IMAGE_BOTTOM_LEFT'],
            mode="wrap"
        )

        # テキストを右上と右下に配置
        self.drawTextWithWrapping(
            draw=draw,
            text=self.data[0]['text'],
            font=font,
            maxWidth=maxWidth,
            startPosition=startPositions['TEXT_TOP_RIGHT'],
            lineHeight=lineHeight,
            fill=fillColor,
            mode="wrap"
        )

        self.drawTextWithWrapping(
            draw=draw,
            text=self.data[1]['text'],
            font=font,
            maxWidth=maxWidth,
            startPosition=startPositions['TEXT_BOTTOM_RIGHT'],
            lineHeight=lineHeight,
            fill=fillColor,
            mode="wrap"
        )


# **********************************************************************************


class PatternCEditor(ImageEditor):
    def editImage(self, baseImage, draw, font, baseWidth, baseHeight):
        # 画像の配置
        maxWidth = ImageInfo.MAX_WIDTH.value
        lineHeight = ImageInfo.LINE_HEIGHT.value
        fillColor = ImageInfo.FILL_COLOR_BLACK.value

        # START_POSITIONS を使用して位置を取得
        startPositions = ImageInfo.START_POSITIONS.value[self.pattern]

        # 画像を2枚配置
        self.drawImageWithMode(
            baseImage=baseImage,
            imagePath=self.data[0]['imagePath'],
            maxWidth=ImageInfo.IMAGE_SIZE_SMALL.value[0],
            maxHeight=ImageInfo.IMAGE_SIZE_SMALL.value[1],
            startPosition=startPositions['IMAGE_TOP_LEFT'],
            mode="wrap"
        )

        self.drawImageWithMode(
            baseImage=baseImage,
            imagePath=self.data[1]['imagePath'],
            maxWidth=ImageInfo.IMAGE_SIZE_SMALL.value[0],
            maxHeight=ImageInfo.IMAGE_SIZE_SMALL.value[1],
            startPosition=startPositions['IMAGE_BOTTOM_LEFT'],
            mode="wrap"
        )

        # テキストを右上と右下に配置
        self.drawTextWithWrapping(
            draw=draw,
            text=self.data[0]['text'],
            font=font,
            maxWidth=maxWidth,
            startPosition=startPositions['TEXT_TOP_RIGHT'],
            lineHeight=lineHeight,
            fill=fillColor,
            mode="wrap"
        )

        self.drawTextWithWrapping(
            draw=draw,
            text=self.data[1]['text'],
            font=font,
            maxWidth=maxWidth,
            startPosition=startPositions['TEXT_BOTTOM_RIGHT'],
            lineHeight=lineHeight,
            fill=fillColor,
            mode="wrap"
        )

# **********************************************************************************


class PatternDEditor(ImageEditor):
    def editImage(self, baseImage, draw, font, baseWidth, baseHeight):
        # 画像の配置
        maxWidth = ImageInfo.MAX_WIDTH.value
        lineHeight = ImageInfo.LINE_HEIGHT.value
        fillColor = ImageInfo.FILL_COLOR_BLACK.value

        # START_POSITIONS を使用して位置を取得
        startPositions = ImageInfo.START_POSITIONS.value[self.pattern]

        # 画像を2枚配置
        self.drawImageWithMode(
            baseImage=baseImage,
            imagePath=self.data[0]['imagePath'],
            maxWidth=ImageInfo.IMAGE_SIZE_SMALL.value[0],
            maxHeight=ImageInfo.IMAGE_SIZE_SMALL.value[1],
            startPosition=startPositions['IMAGE_TOP_LEFT'],
            mode="wrap"
        )

        self.drawImageWithMode(
            baseImage=baseImage,
            imagePath=self.data[1]['imagePath'],
            maxWidth=ImageInfo.IMAGE_SIZE_SMALL.value[0],
            maxHeight=ImageInfo.IMAGE_SIZE_SMALL.value[1],
            startPosition=startPositions['IMAGE_BOTTOM_LEFT'],
            mode="wrap"
        )

        # テキストを右上と右下に配置
        self.drawTextWithWrapping(
            draw=draw,
            text=self.data[0]['text'],
            font=font,
            maxWidth=maxWidth,
            startPosition=startPositions['TEXT_TOP_RIGHT'],
            lineHeight=lineHeight,
            fill=fillColor,
            mode="wrap"
        )

        self.drawTextWithWrapping(
            draw=draw,
            text=self.data[1]['text'],
            font=font,
            maxWidth=maxWidth,
            startPosition=startPositions['TEXT_BOTTOM_RIGHT'],
            lineHeight=lineHeight,
            fill=fillColor,
            mode="wrap"
        )

# **********************************************************************************
