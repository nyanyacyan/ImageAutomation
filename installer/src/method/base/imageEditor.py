# coding: utf-8
# $$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$

# $$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$
# import
import os, requests
from selenium.webdriver.chrome.webdriver import WebDriver
from PIL import Image, ImageDraw, ImageFont

# 自作モジュール
from .utils import Logger
from constElementPath import ImageInfo


# $$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$
# **********************************************************************************


class ImageEditor:
    requiredImages = {}
    def __init__(self, pattern: str, data: list, debugMode=True):
        # logger
        self.getLogger = Logger(__name__, debugMode=debugMode)
        self.logger = self.getLogger.getLogger()

        self.pattern = pattern
        self.data = data[pattern]

        self.baseImagePath = ImageInfo.IMAGE_PATH.value[{pattern}]
        self.fontSize = ImageInfo.FONT_SIZES.value[{pattern}]
        self.imageNum = ImageInfo.FONT_SIZES.value[{pattern}]

        self.imageSize = (1080, 1080)


# ----------------------------------------------------------------------------------
# 画像が揃っているかチェック

    def checkImageUrl(self):
        for item in self.data:
            try:
                # allow_redirects=Trueは短縮URLなどリダイレクトされてることがあること自動許可する
                response = requests.head(item['imagePath'], allow_redirects=True)
                if response.status_code < 200 or response.status_code >= 400:
                    self.logger.error(f"{self.pattern} の画像が見つかりません: \n{item['image_path']}")
                    return False
            except requests.RequestException as e:
                self.logger.error(f"{self.pattern} の画像データにアクセスできません。: \n{item['image_path']}\nエラー: {e}")
                return False

            return True


# ----------------------------------------------------------------------------------


    def checkImageCount(self):
        if len(self.data) < self.imageNum[self.pattern]:
            self.logger.error(f"{self.pattern} に必要な画像枚数が不足しています。\n必要: {self.required_images[self.pattern]}\n実際: {len(self.data)}")
            return False
        return True


# ----------------------------------------------------------------------------------


    def editImage(self, baseImage, draw, font, width, height):
        raise NotImplementedError("サブクラスはこのメソッドを実装する必要があります。")



# ----------------------------------------------------------------------------------


    def createImage(self, fontPath: str, outputPath: str):
        if not self.checkImageCount():
            return False
        if not self.checkImageUrl():
            return False

        baseImage = Image.open(self.baseImagePath).resize(self.imageSize).convert("RGBA")
        width, height = baseImage.size
        draw = ImageDraw.Draw(baseImage)
        font = ImageFont.truetype(fontPath, self.fontSize)

        self.editImage(baseImage, draw, font, width, height)

        outputFilePath = os.path.join(outputPath, f"output_{self.pattern}.png")

        baseImage.save(outputFilePath, format="PNG")
        self.logger.info(f"保存完了: {outputFilePath}")
        return True


# ----------------------------------------------------------------------------------
