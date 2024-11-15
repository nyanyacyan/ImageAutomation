# coding: utf-8
# $$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$

# $$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$
# import
import os, requests
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
            fontColor = ImageInfo.FONT_COLORS.value[pattern]  # パターンに対応するフォントカラーを取得

            # 画像作成メソッドにパターン固有の情報を渡す
            if not self.createImage(pattern_data, fontPath, baseImagePath, fontSize, outputFolder, pattern, fontColor):
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


    def createImage(self, data: dict, fontPath: str, baseImagePath: str, fontSize: int, outputFolder: str, pattern: str, fontColor: Tuple[int, int, int]):
        '''
        fontPath→使用したいフォントを指定する
        baseImagePath→ベース画像を指定する
        '''
        self.logger.info(f"createImage 呼び出し時の {pattern} の data の型: {type(data)}")
        self.logger.info(f"createImage 呼び出し時の {pattern} の data の内容: {data}")

        # 画像データが揃っているかをチェック
        if not self.checkImageAndTextCount(data, pattern):
            return False

        # ベース画像の読み込み
        baseImage = Image.open(baseImagePath).resize(self.imageSize).convert("RGBA")
        draw = ImageDraw.Draw(baseImage)
        font = ImageFont.truetype(fontPath, fontSize)

        # 各パターンの配置情報を取得
        positions = ImageInfo.POSITIONS.value[pattern]

        # 画像の配置
        if pattern == 'A':
            # Pattern A の場合
            if 'imagePath_1' in data:
                self.drawImageWithMode(baseImage, data['imagePath_1'], positions['IMAGE_CENTER'])

            # フォントサイズを自動調整して text_1, text_2 を縦書きで描画
            if 'text_1' in data and 'TEXT_RIGHT_TOP' in positions:
                self.drawVerticalTextWithOutline(draw, data['text_1'], font, positions['TEXT_RIGHT_TOP'], fill=fontColor, center=True)

            if 'text_2' in data and 'TEXT_RIGHT_BOTTOM' in positions:
                self.drawVerticalTextWithOutline(draw, data['text_2'], font, positions['TEXT_RIGHT_BOTTOM'], fill=fontColor, center=True)

            # text_3 は通常の横書き
            if 'text_3' in data and 'TEXT_BOTTOM' in positions:
                self.drawTextWithOutline(draw, data['text_3'], positions['TEXT_BOTTOM'], font, fill=fontColor, lineHeight=40)

        else:
            # Pattern B, C, D の場合
            if 'imagePath_1' in data:
                self.drawImageWithMode(baseImage, data['imagePath_1'], positions['IMAGE_TOP_LEFT'])

            if 'imagePath_2' in data:
                self.drawImageWithMode(baseImage, data['imagePath_2'], positions['IMAGE_BOTTOM_LEFT'])

            # テキストの配置
            if 'text_1' in data and 'TEXT_TOP_RIGHT' in positions:
                self.drawTextWithOutline(draw, data['text_1'], positions['TEXT_TOP_RIGHT'], font, fill=fontColor, lineHeight=40)

            if 'text_2' in data and 'TEXT_BOTTOM_RIGHT' in positions:
                self.drawTextWithOutline(draw, data['text_2'], positions['TEXT_BOTTOM_RIGHT'], font, fill=fontColor, lineHeight=40)

        # 画像の保存
        outputFilePath = os.path.join(outputFolder, f"output_{pattern}.png")
        baseImage.save(outputFilePath, format="PNG")
        self.logger.info(f"保存完了: {outputFilePath}")

        return True



# ----------------------------------------------------------------------------------


    def drawTextWithOutline(
            self,
            draw: ImageDraw.ImageDraw,
            text: str,
            boundingBox: Tuple[int, int, int, int],
            font: ImageFont.FreeTypeFont,
            lineHeight: int,
            fill: Tuple[int, int, int] = ImageInfo.FILL_COLOR_BLACK.value,
            outline_fill: Tuple[int, int, int] = (255, 255, 255),
            outline_width: int = 2
        ):
        """
        アウトライン付きのテキストを描画します。
        """
        # バウンディングボックスの幅と高さを取得
        box_width = boundingBox[2] - boundingBox[0]
        box_height = boundingBox[3] - boundingBox[1]

        # 初期位置をバウンディングボックスの上側に設定
        x = boundingBox[0]
        y = boundingBox[1]

        # テキストのアウトラインを描画
        for offset_x in range(-outline_width, outline_width + 1):
            for offset_y in range(-outline_width, outline_width + 1):
                if offset_x == 0 and offset_y == 0:
                    continue
                draw.text((x + offset_x, y + offset_y), text, font=font, fill=outline_fill)

        # テキスト本体を描画
        draw.text((x, y), text, font=font, fill=fill)


# ----------------------------------------------------------------------------------


    def drawVerticalTextWithOutline(
            self,
            draw: ImageDraw.ImageDraw,
            text: str,
            font: ImageFont.FreeTypeFont,
            boundingBox: Tuple[int, int, int, int],
            fill: Tuple[int, int, int] = (0, 0, 0),
            outline_fill: Tuple[int, int, int] = (255, 255, 255),
            outline_width: int = 2,
            center: bool = False
        ):
        """
        縦書きのテキストをアウトライン付きで描画します。
        """
        # バウンディングボックスの幅と高さを取得
        box_width = boundingBox[2] - boundingBox[0]
        box_height = boundingBox[3] - boundingBox[1]

        # 初期位置をバウンディングボックスの上側に設定
        x = boundingBox[0]
        y = boundingBox[1]

        # テキストを改行するために文字ごとに分割
        text_lines = [char for char in text]

        # 各文字の高さを取得し、文字間を詰めるために倍率を調整
        char_height = font.getbbox('あ')[3]  # 任意の文字で高さを取得
        line_spacing = char_height * 0.9  # 文字間を詰める（0.9倍の間隔）

        # テキスト全体の高さを計算
        total_text_height = len(text_lines) * line_spacing

        # テキストの中央揃えを行う
        if center:
            y += int((box_height - total_text_height) // 2)

        # 各行を描画
        for index, line in enumerate(text_lines):
            char_x = x
            char_y = y + int(index * line_spacing)

            # バウンディングボックスの高さを超えないように描画する
            if char_y + char_height > boundingBox[3]:
                break

            # 文字の幅を取得して、中央に揃えるための調整を行う
            char_width = font.getbbox(line)[2]

            # 数字などの特定の文字に対して、少し中央に寄せる補正を行う
            if line.isdigit():
                adjusted_x = char_x + (box_width - char_width) // 2 - 5  # 数字の位置を微調整（-5など適宜調整）
            else:
                adjusted_x = char_x + (box_width - char_width) // 2

            # アウトラインの描画
            for offset_x in range(-outline_width, outline_width + 1):
                for offset_y in range(-outline_width, outline_width + 1):
                    if offset_x == 0 and offset_y == 0:
                        continue
                    draw.text((adjusted_x + offset_x, char_y + offset_y), line, font=font, fill=outline_fill, direction='ttb')

            # テキスト本体を描画
            draw.text((adjusted_x, char_y), line, font=font, fill=fill, direction='ttb')






# ----------------------------------------------------------------------------------


    def drawVerticalText(self, draw: ImageDraw.ImageDraw, text: str, font: ImageFont.FreeTypeFont, boundingBox: Tuple[int, int, int, int], lineHeight: int, fill: Tuple[int, int, int] = (0, 0, 0), center: bool = False):
        """
        縦書きのテキストを描画します。
        """
        # バウンディングボックスの幅と高さを取得
        box_width = boundingBox[2] - boundingBox[0]
        box_height = boundingBox[3] - boundingBox[1]

        # 初期位置をバウンディングボックスの上側に設定
        x = boundingBox[0]
        y = boundingBox[1]

        # 縦書きのため、文字ごとに描画
        total_text_height = len(text) * lineHeight

        # テキストの中央揃えを行う
        if center:
            y += (box_height - total_text_height) // 2

        for char in text:
            char_bbox = font.getbbox(char)
            char_width = char_bbox[2] - char_bbox[0]
            char_height = char_bbox[3] - char_bbox[1]

            if center:
                centered_x = x + (box_width - char_width) // 2
            else:
                centered_x = x

            if y + char_height <= boundingBox[1] + box_height:  # ボックスの下限を超えない場合のみ描画
                draw.text((centered_x, y), char, font=font, fill=fill)
                y += lineHeight



# ----------------------------------------------------------------------------------


    def drawTextWithWrapping(
            self,
            draw: ImageDraw.ImageDraw,
            text: str,
            font: ImageFont.FreeTypeFont,
            boundingBox: Tuple[int, int, int, int],  # (x1, y1, x2, y2) のタプル
            lineHeight: int,
            fill: Tuple[int, int, int] = (0, 0, 0),
            mode: str = "wrap"
        ):
        # バウンディングボックスの幅と高さを取得
        box_width = boundingBox[2] - boundingBox[0]
        box_height = boundingBox[3] - boundingBox[1]

        # テキスト全体の高さを計算し、枠に収まるようにフォントサイズを調整
        y = boundingBox[1]
        lines = []
        current_line = ""

        for char in text:
            # 1文字ずつ追加して高さを計算
            if draw.textbbox((0, 0), current_line + char, font=font)[3] + lineHeight <= box_height:
                current_line += char
            else:
                # 枠の高さを超える場合は新しい行を追加
                lines.append(current_line)
                current_line = char

        if current_line:
            lines.append(current_line)

        # テキストの中央揃えを行うための初期位置の計算
        total_text_height = len(lines) * lineHeight
        y = boundingBox[1] + (box_height - total_text_height) // 2  # 縦の中央揃え

        # 各行を描画
        for line in lines:
            # 各行を横に中央揃え
            line_width = draw.textlength(line, font=font)
            x = boundingBox[0] + (box_width - line_width) // 2

            draw.text((x, y), line, font=font, fill=fill)
            y += lineHeight



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
    'imagePath_1': 'https://property.es-img.jp/rent/img/1136293183700000023966/0000000001136293183700000023966_10.jpg?iid=509482932',
    'text_1': '千歳烏山駅',
    'text_2': '徒歩3分',
    'text_3': '京王電鉄 高速高尾線'
}

data_B = {
    'imagePath_1': 'https://property.es-img.jp/rent/img/100000000000000000000009940467/0100000000000000000000009940467_1.jpg?iid=2733185228',
    'imagePath_2': 'https://property.es-img.jp/rent/img/100000000000000000000009940467/0100000000000000000000009940467_21.jpg?iid=1891244155',
    'text_1': '••　モニタ付インターホン\n•　システムキッチン\n•　2口コンロ\n•　ガスコンロ',
    'text_2': 'モニターが付いていることで、訪問者を事前に確認でき、不審者を防ぐことができます。特に賃貸物件では、他人と共有する空間が多いため、安心感が増します。'
}

data_C = {
    'imagePath_1': 'https://property.es-img.jp/rent/img/100000000000000000000009940467/0100000000000000000000009940467_3.jpg?iid=2321422476',
    'imagePath_2': 'https://property.es-img.jp/rent/img/100000000000000000000009940467/0100000000000000000000009940467_15.jpg?iid=2672302265',
    'text_1': '•　モニタ付インターホン\n•　システムキッチン\n•　2口コンロ\n•　ガスコンロ',
    'text_2': 'モニターが付いていることで、訪問者を事前に確認でき、不審者を防ぐことができます。特に賃貸物件では、他人と共有する空間が多いため、安心感が増します。'
}

data_D = {
    'imagePath_1': 'https://property.es-img.jp/rent/img/100000000000000000000009940467/0100000000000000000000009940467_14.jpg?iid=3087538415',
    'imagePath_2': 'https://property.es-img.jp/rent/img/100000000000000000000009940467/0100000000000000000000009940467_4.jpg?iid=2328631444',
    'text_1': '••　モニタ付インターホン\n•　システムキッチン\n•　2口コンロ\n•　ガスコンロ',
    'text_2': 'モニターが付いていることで、訪問者を事前に確認でき、不審者を防ぐことができます。特に賃貸物件では、他人と共有する空間が多いため、安心感が増します。'
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
