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

        # パターンごとの必要な画像とテキストの数を定義
        pattern_requirements = {
            'A': {'images': 1, 'texts': 3},
            'B': {'images': 2, 'texts': 2},
            'C': {'images': 2, 'texts': 2},
            'D': {'images': 2, 'texts': 2}
        }

        for pattern in patterns:
            if pattern not in data:
                self.logger.error(f"{pattern} パターンのデータが欠けているため、{pattern} とそれ以降のすべてのパターンをスキップします。")
                break

            # パターン固有のデータを取得
            pattern_data = data[pattern]
            baseImagePath = ImageInfo.BASE_IMAGE_PATH.value[pattern]
            fontSize = ImageInfo.FONT_SIZES.value[pattern]
            fontPath = ImageInfo.FONT_PATH.value
            outputFolder = ImageInfo.OUTPUT_PATH.value

            # パターンごとの画像とテキストの数を確認
            # requirements = pattern_requirements[pattern]
            # if not self.checkImageCount(pattern_data, pattern):
            #     self.logger.error(f"{pattern} のデータが不足しているため、スキップします。")
            #     continue

            # 画像作成メソッドにパターン固有の情報を渡す
            if not self.createImage(pattern_data, fontPath, baseImagePath, fontSize, outputFolder, pattern):
                self.logger.error(f"パターン {pattern} の画像データが揃ってないため、以降のパターンをスキップします。")
                break

        self.logger.info(f"画像処理が完了しました。")



# ----------------------------------------------------------------------------------


    def checkImageAndTextCount(self, data: dict, pattern: str):
        # 必要な項目をパターンごとに定義
        required_keys = {
            'A': ['imagePath_1', 'text_1', 'text_2', 'text_3'],
            'B': ['imagePath_1', 'imagePath_2', 'text_1', 'text_2'],
            'C': ['imagePath_1', 'imagePath_2', 'text_1', 'text_2'],
            'D': ['imagePath_1', 'imagePath_2', 'text_1', 'text_2']
        }

        # 必要なキーが存在し、かつそのキーに値があるかをチェック
        missing_or_empty_keys = [key for key in required_keys[pattern] if key not in data or not data[key]]

        if missing_or_empty_keys:
            self.logger.error(f"{pattern} に必要なデータが不足しています。欠けているキーまたは空のキー: {missing_or_empty_keys}")
            return False

        # imagePath の有効性をチェック
        image_keys = [key for key in required_keys[pattern] if 'imagePath' in key]
        for key in image_keys:
            try:
                response = requests.head(data[key], allow_redirects=True)
                if response.status_code < 200 or response.status_code >= 400:
                    self.logger.error(f"{pattern} の画像が見つかりません: \n{data[key]}")
                    return False
            except requests.RequestException as e:
                self.logger.error(f"{pattern} の画像データにアクセスできません: \n{data[key]}\nエラー: {e}")
                return False

        return True


# ----------------------------------------------------------------------------------


    def createImage(self, data: dict, fontPath: str, baseImagePath: str, fontSize: int, outputFolder: str, pattern: str):
        '''
        fontPath→使用したいフォントを指定する
        baseImagePath→ベース画像を指定する
        '''
        self.logger.info(f"createImage 呼び出し時の {pattern} の data の型: {type(data)}")
        self.logger.info(f"createImage 呼び出し時の {pattern} の data の内容: {data}")

        # 画像データが揃っているかをチェック
        if not self.checkImageAndTextCount(data, pattern):  # ここで pattern 引数を追加
            return False

        # ベース画像の読み込み
        print(f"baseImagePath: {baseImagePath}")
        baseImage = Image.open(baseImagePath).resize(self.imageSize).convert("RGBA")
        draw = ImageDraw.Draw(baseImage)
        font = ImageFont.truetype(fontPath, fontSize)

        # 各パターンの配置情報を取得
        positions = ImageInfo.POSITIONS.value[pattern]

        # 画像の配置
        if pattern == 'A':
            if 'imagePath_1' in data:
                if 'IMAGE_CENTER' in positions:
                    self.drawImageWithMode(baseImage, data['imagePath_1'], positions['IMAGE_CENTER'])
        elif pattern in ['B', 'C', 'D']:
            if 'imagePath_1' in data:
                if 'IMAGE_TOP_LEFT' in positions:
                    self.drawImageWithMode(baseImage, data['imagePath_1'], positions['IMAGE_TOP_LEFT'])
            if 'imagePath_2' in data:
                if 'IMAGE_BOTTOM_LEFT' in positions:
                    self.drawImageWithMode(baseImage, data['imagePath_2'], positions['IMAGE_BOTTOM_LEFT'])

        # テキストの配置
        if 'text_1' in data and 'TEXT_RIGHT_TOP' in positions:
            self.drawTextWithWrapping(draw, data['text_1'], font, positions['TEXT_RIGHT_TOP'], 40)

        if 'text_2' in data and 'TEXT_RIGHT_BOTTOM' in positions:
            self.drawTextWithWrapping(draw, data['text_2'], font, positions['TEXT_RIGHT_BOTTOM'], 40)

        if 'text_3' in data and 'TEXT_BOTTOM' in positions:
            self.drawTextWithWrapping(draw, data['text_3'], font, positions['TEXT_BOTTOM'], 40)

        # 画像の保存
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
            boundingBox: Tuple[int, int, int, int],  # 新しいパラメータ、(x1, y1, x2, y2) のタプル
            lineHeight: int,
            fill: Tuple[int, int, int] = (0, 0, 0),
            mode: str = "wrap"
        ):
        # バウンディングボックスの幅と高さを取得
        box_width = boundingBox[2] - boundingBox[0]
        box_height = boundingBox[3] - boundingBox[1]

        # 初期位置をバウンディングボックスの上側に設定
        x = boundingBox[0]
        y = boundingBox[1]

        lines = []

        if mode == "center":
            self.log(f"textを中央に合わせて配置(改行で区切る): {text}")
            # 手動改行に基づいて行を分割し、各行を中央揃え
            lines = text.split('\n')
            for line in lines:
                lineWidth = draw.textlength(line, font=font)
                centered_x = x + (box_width - lineWidth) // 2
                if y + lineHeight <= boundingBox[1] + box_height:  # ボックスの下限を超えない場合のみ描画
                    draw.text((centered_x, y), line, font=font, fill=fill)
                    y += lineHeight

        elif mode == "wrap":
            self.logger.info(f"文字を埋めていく(区切りなし): {text}")

            line = ""
            # テキストを1文字ずつ追加し、最大幅を超えたら改行
            for char in text:
                # 現在の行に文字を追加して幅をチェック
                if draw.textlength(line + char, font=font) <= box_width:
                    line += char
                else:
                    # 最大幅を超えた場合、行を確定して次の行に移る
                    if y + lineHeight <= boundingBox[1] + box_height:  # ボックスの下限を超えない場合のみ描画
                        draw.text((x, y), line, font=font, fill=fill)
                        y += lineHeight
                    line = char  # 次の行の最初の文字として設定
            # 最後の行を描画
            if line:
                if y + lineHeight <= boundingBox[1] + box_height:  # ボックスの下限を超えない場合のみ描画
                    draw.text((x, y), line, font=font, fill=fill)


# ----------------------------------------------------------------------------------


    def drawImageWithMode(
            self,
            baseImage: Image.Image,
            imagePath: str,
            boundingBox: Tuple[int, int, int, int],  # 新しいパラメータ、(x1, y1, x2, y2) のタプル
        ):
        # 画像を取得して `insertImage` を定義する
        if imagePath.startswith("http://") or imagePath.startswith("https://"):
            try:
                response = requests.get(imagePath, stream=True)
                response.raise_for_status()
                insertImage = Image.open(BytesIO(response.content)).convert("RGBA")
            except requests.RequestException as e:
                self.log(f"画像の取得に失敗しました: {imagePath}\nエラー: {e}")
                return
        else:
            try:
                insertImage = Image.open(imagePath).convert("RGBA")
            except FileNotFoundError:
                self.log(f"ローカル画像ファイルが見つかりません: {imagePath}")
                return

        # バウンディングボックスの幅と高さを取得
        box_width = boundingBox[2] - boundingBox[0]
        box_height = boundingBox[3] - boundingBox[1]

        # 画像のリサイズ（アスペクト比を保ちながら枠に収める）
        insert_width, insert_height = insertImage.size
        aspect_ratio = insert_width / insert_height

        # ボックスに収まるようにリサイズ
        if (box_width / box_height) > aspect_ratio:
            # ボックスの幅に対して画像が細長い場合
            new_height = box_height
            new_width = int(new_height * aspect_ratio)
        else:
            # ボックスの高さに対して画像が幅広い場合
            new_width = box_width
            new_height = int(new_width / aspect_ratio)

        insertImage = insertImage.resize((new_width, new_height), Image.LANCZOS)

        # 画像を貼り付ける位置を決定する
        x_offset = boundingBox[0] + (box_width - new_width) // 2
        y_offset = boundingBox[1] + (box_height - new_height) // 2

        # 画像の貼り付け
        baseImage.paste(insertImage, (x_offset, y_offset), insertImage)



# ----------------------------------------------------------------------------------


data_A = {
    'imagePath_1': 'https://property.es-img.jp/rent/img/100000000000000000000009940467/0100000000000000000000009940467_10.jpg?iid=2297698464',
    'text_1': '京王線',
    'text_2': '徒歩3分',
    'text_3': '調布駅'
}

data_B = {
    'imagePath_1': 'https://property.es-img.jp/rent/img/100000000000000000000009940467/0100000000000000000000009940467_1.jpg?iid=2733185228',
    'imagePath_2': 'https://property.es-img.jp/rent/img/100000000000000000000009940467/0100000000000000000000009940467_21.jpg?iid=1891244155',
    'text_1': 'テキストB1',
    'text_2': 'テキストB2'
}

data_C = {
    'imagePath_1': 'https://property.es-img.jp/rent/img/100000000000000000000009940467/0100000000000000000000009940467_3.jpg?iid=2321422476',
    'imagePath_2': 'https://property.es-img.jp/rent/img/100000000000000000000009940467/0100000000000000000000009940467_15.jpg?iid=2672302265',
    'text_1': 'テキストC1',
    'text_2': 'テキストC2'
}

data_D = {
    'imagePath_1': 'https://property.es-img.jp/rent/img/100000000000000000000009940467/0100000000000000000000009940467_14.jpg?iid=3087538415',
    'imagePath_2': 'https://property.es-img.jp/rent/img/100000000000000000000009940467/0100000000000000000000009940467_4.jpg?iid=2328631444',
    'text_1': 'テキストD1',
    'text_2': 'テキストD2'
}

# 各データをパターンごとにまとめる辞書
data = {
    'A': data_A,
    'B': data_B,
    'C': data_C,
    'D': data_D
}




# Instantiate the main ImageEditor class and execute pattern editors
if __name__ == "__main__":
    image_editor = ImageEditor(debugMode=True)
    image_editor.executePatternEditors(data)
