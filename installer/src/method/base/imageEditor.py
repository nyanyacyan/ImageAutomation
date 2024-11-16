# coding: utf-8
# $$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$

# $$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$
# import
import os, requests, traceback
from PIL import Image, ImageDraw, ImageFont
from typing import Tuple, List
from io import BytesIO


# 自作モジュール
from utils import Logger
from path import BaseToPath
from method.constElementPath import ImageInfo


# $$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$
# **********************************************************************************


class ImageEditor:
    def __init__(self, debugMode=True):
        # logger
        self.getLogger = Logger(__name__, debugMode=debugMode)
        self.logger = self.getLogger.getLogger()

        self.path = BaseToPath(debugMode=debugMode)

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
            fontFileName = ImageInfo.FONT_NAME.value
            fontPath = self.inputDataFolderPath(fileName=fontFileName)
            outputFolder = self.resultOutputFilePath
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
            'A': ['imagePath_1', 'text_1', 'text_2'],
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
        base_image = Image.open(baseImagePath).resize(self.imageSize).convert("RGBA")

        # 各パターンの配置情報を取得
        positions = ImageInfo.POSITIONS.value[pattern]

        # 画像の配置
        if pattern == 'A':
            # Pattern A の場合
            if 'imagePath_1' in data:
                # 1. Image1 の配置
                self.drawImageWithMode(base_image, data['imagePath_1'], positions['IMAGE_CENTER'])

            # 2. 半透明のラインの描画（BACK_BOTTOM）
            if "BACK_BOTTOM" in positions:
                back_bottom_box = positions["BACK_BOTTOM"]

                # ライン用の新しい透明なレイヤーを作成
                overlay = Image.new('RGBA', base_image.size, (255, 255, 255, 0))
                overlay_draw = ImageDraw.Draw(overlay)

                # 半透明のラインを描画
                overlay_draw.rectangle(back_bottom_box, fill=(255, 255, 255, 150))

                # ベース画像とラインを合成
                base_image = Image.alpha_composite(base_image, overlay)

            # 3. テキストの配置
            draw = ImageDraw.Draw(base_image)
            font = ImageFont.truetype(fontPath, fontSize)

            # テキスト1を右揃えで配置（アウトライン付き）
            if 'text_1' in data and 'TEXT_RIGHT_TOP' in positions:
                self.drawTextWithOutlineRightAligned(draw, data['text_1'], positions['TEXT_RIGHT_TOP'], font, fill=fontColor, outline_fill=(255, 255, 255), outline_width=2)

            # テキスト2を枠の中央に配置（アウトライン付き）
            if 'text_2' in data and 'TEXT_BOTTOM_LEFT' in positions:
                self.drawTextWithOutline(draw, data['text_2'], positions['TEXT_BOTTOM_LEFT'], fontPath, initialFontSize=fontSize, lineHeight=fontSize, fill=fontColor, outline_fill=(255, 255, 255), outline_width=2, center=False)

            # テキスト3は通常の横書き（アウトライン付き）
            if 'text_3' in data and 'TEXT_BOTTOM_RIGHT' in positions:
                self.drawTextWithOutline(draw, data['text_3'], positions['TEXT_BOTTOM_RIGHT'], fontPath, initialFontSize=fontSize, lineHeight=40, fill=fontColor, outline_fill=(255, 255, 255), outline_width=2)

        else:
            # Pattern B, C, D の場合
            if 'imagePath_1' in data:
                self.drawImageWithMode(base_image, data['imagePath_1'], positions['IMAGE_TOP_LEFT'])

            if 'imagePath_2' in data:
                self.drawImageWithMode(base_image, data['imagePath_2'], positions['IMAGE_BOTTOM_LEFT'])

            # テキストの配置
            draw = ImageDraw.Draw(base_image)
            if 'text_1' in data and 'TEXT_TOP_RIGHT' in positions:
                self.drawTextWithOutline(draw, data['text_1'], positions['TEXT_TOP_RIGHT'], fontPath, initialFontSize=fontSize, fill=fontColor, lineHeight=40, outline_fill=(255, 255, 255), outline_width=2)

            if 'text_2' in data and 'TEXT_BOTTOM_RIGHT' in positions:
                self.drawTextWithOutline(draw, data['text_2'], positions['TEXT_BOTTOM_RIGHT'], fontPath, initialFontSize=fontSize, fill=fontColor, lineHeight=40, outline_fill=(255, 255, 255), outline_width=2)

        # 画像の保存
        outputFilePath = os.path.join(outputFolder, f"output_{pattern}.png")
        base_image.save(outputFilePath, format="PNG")
        self.logger.info(f"保存完了: {outputFilePath}")

        return True


# ----------------------------------------------------------------------------------


    def drawTextWithOutlineRightAligned(self, draw: ImageDraw.ImageDraw, text: str, boundingBox: Tuple[int, int, int, int], font: ImageFont.FreeTypeFont, fill: Tuple[int, int, int], outline_fill: Tuple[int, int, int] = (0, 0, 0), outline_width: int = 2):
        """
        テキストを右揃えにしてアウトライン付きで描画します。
        """
        # バウンディングボックスの幅と高さを取得
        box_width = boundingBox[2] - boundingBox[0]
        box_height = boundingBox[3] - boundingBox[1]

        # テキストの幅を取得し、右揃えの位置を計算
        text_width = draw.textlength(text, font=font)
        x = boundingBox[2] - text_width
        y = boundingBox[1]

        # アウトラインの描画
        for offset_x in range(-outline_width, outline_width + 1):
            for offset_y in range(-outline_width, outline_width + 1):
                if offset_x == 0 and offset_y == 0:
                    continue
                draw.text((x + offset_x, y + offset_y), text, font=font, fill=outline_fill)

        # テキスト本体を描画
        draw.text((x, y), text, font=font, fill=fill)


# ----------------------------------------------------------------------------------


    def drawTextWithOutline(
            self,
            draw: ImageDraw.ImageDraw,
            text: str,
            boundingBox: Tuple[int, int, int, int],
            font_file_path: str,
            initialFontSize: int,
            lineHeight: int,
            fill: Tuple[int, int, int] = (0, 0, 0),
            outline_fill: Tuple[int, int, int] = (255, 255, 255),
            outline_width: int = 2,
            center: bool = False  # この行を追加
        ):
        """
        アウトライン付きのテキストを描画し、必要であればフォントサイズを小さくして枠に収まるように調整します。
        """
        # バウンディングボックスの幅と高さを取得
        box_width = boundingBox[2] - boundingBox[0]
        box_height = boundingBox[3] - boundingBox[1]

        # 初期フォントサイズから開始
        font_size = initialFontSize
        font_path_str = str(font_file_path)
        font = ImageFont.truetype(font_path_str, font_size)

        # フォントサイズを調整して枠に収める
        while True:
            text_width, text_height = draw.textbbox((0, 0), text, font=font)[2:4]
            if text_width <= box_width and text_height <= box_height:
                break
            font_size -= 2
            if font_size <= 0:  # 最小フォントサイズを超えた場合
                self.logger.error(f"テキスト '{text}' を枠に収めるのに十分なフォントサイズが見つかりません。")
                return
            font = ImageFont.truetype(font_path_str, font_size)

        # 初期位置を設定
        x = boundingBox[0]
        y = boundingBox[1]

        # 中央揃えオプション
        if center:
            x += (box_width - text_width) // 2
            y += (box_height - text_height) // 2

        # アウトラインの描画
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
        縦書きのテキストをアウトライン付きで描画し、必要に応じてフォントサイズを調整します。
        """
        # バウンディングボックスの幅と高さを取得
        box_width = boundingBox[2] - boundingBox[0]
        box_height = boundingBox[3] - boundingBox[1]

        # 初期フォントサイズ
        font_size = font.size

        # 各文字の高さを取得し、文字間を詰めるために倍率を調整
        line_spacing = font.getbbox('あ')[3] * 0.9  # 任意の文字で高さを取得し、間隔を少し詰める
        total_text_height = len(text) * line_spacing

        # 枠内に収まるようにフォントサイズを調整
        while total_text_height > box_height and font_size > 10:
            font_size -= 2
            font = ImageFont.truetype(font.path, font_size)  # フォントサイズを更新
            line_spacing = font.getbbox('あ')[3] * 0.9
            total_text_height = len(text) * line_spacing

        # 初期位置をバウンディングボックスの上側に設定
        x = boundingBox[0]
        y = boundingBox[1]

        # テキストの中央揃えを行う
        if center:
            y += int((box_height - total_text_height) // 2)

        # 各行を描画
        for index, line in enumerate(text):
            char_x = x
            char_y = y + int(index * line_spacing)

            # バウンディングボックスの高さを超えないように描画する
            if char_y + line_spacing > boundingBox[3]:
                break

            # 文字の幅と高さを取得して、中央に揃えるための調整を行う
            char_bbox = font.getbbox(line)
            char_width = char_bbox[2] - char_bbox[0]
            char_height = char_bbox[3] - char_bbox[1]

            # 記号や数字など、特定の文字に対しては位置を微調整
            adjusted_x = x + (box_width - char_width) // 2
            if line in "・ー−〜、。":
                # 記号の場合、横の中央に揃うように調整
                adjusted_x += 2  # 適宜調整

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
# resultOutput

    @property
    def resultOutputFilePath(self):
        return self.path.getResultOutputPath()


# ----------------------------------------------------------------------------------


    def inputDataFolderPath(self, fileName: str):
        return self.path.getInputDataFilePath(fileName=fileName)


# ----------------------------------------------------------------------------------


data_A = {
    'imagePath_1': 'https://property.es-img.jp/rent/img/1136293183700000023966/0000000001136293183700000023966_10.jpg?iid=509482932',
    'text_1': '東京臨海高速鉄道りんかい線',
    'text_2': '江田駅    徒歩30分',
    'text_3': ''
}

data_B = {
    'imagePath_1': 'https://property.es-img.jp/rent/img/1136293183700000019925/0000000001136293183700000019925_1.jpg?iid=4032567125',
    'imagePath_2': 'https://property.es-img.jp/rent/img/1136293183700000019925/0000000001136293183700000019925_23.jpg?iid=3611105031',
    'text_1': '•　モニタ付インターホン\n\n•　システムキッチン\n\n•　2口コンロ\n\n•　ガスコンロ',
    'text_2': 'モニターが付いていることで、訪問者を事前に確認でき、不審者を防ぐことができます。特に賃貸物件では、他人と共有する空間が多いため、安心感が増します。'
}

data_C = {
    'imagePath_1': 'https://property.es-img.jp/rent/img/1136293183700000019925/0000000001136293183700000019925_6.jpg?iid=3655407388',
    'imagePath_2': 'https://property.es-img.jp/rent/img/1136293183700000019925/0000000001136293183700000019925_13.jpg?iid=119543694',
    'text_1': '•　モニタ付インターホン\n\n•　システムキッチン\n\n•　2口コンロ\n\n•　ガスコンロ',
    'text_2': 'モニターが付いていることで、訪問者を事前に確認でき、不審者を防ぐことができます。特に賃貸物件では、他人と共有する空間が多いため、安心感が増します。'
}

data_D = {
    'imagePath_1': 'https://property.es-img.jp/rent/img/1136293183700000019925/0000000001136293183700000019925_3.jpg?iid=3660388147',
    'imagePath_2': 'https://property.es-img.jp/rent/img/1136293183700000019925/0000000001136293183700000019925_5.jpg?iid=147986314',
    'text_1': '•　モニタ付インターホン\n\n•　システムキッチン\n\n•　2口コンロ\n\n•　ガスコンロ',
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
