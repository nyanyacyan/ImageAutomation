# coding: utf-8
# $$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$

# $$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$
# import
from PIL import Image, ImageDraw


from utils import Logger
from installer.src.method.constElementPath import ImageInfo


# **********************************************************************************


class ImageGuideDrawer:
    def __init__(self, base_image_path, output_path, debugMode):
        # logger
        self.getLogger = Logger(__name__, debugMode=debugMode)
        self.logger = self.getLogger.getLogger()

        self.base_image_path = base_image_path
        self.output_path = output_path


# ----------------------------------------------------------------------------------


    def draw_guides(self, guide_boxes):
        # ベース画像の読み込み
        base_image_size = ImageInfo.BASE_IMAGE_SIZE.value
        base_image = Image.open(self.base_image_path).resize(base_image_size).convert("RGBA")

        # Drawオブジェクトの作成
        draw = ImageDraw.Draw(base_image)

        # ガイド線を描画
        for box in guide_boxes:
            draw.rectangle(box, outline="red", width=3)  # ガイド線を描画（赤色で幅3）

        # ガイド線が描かれた画像を保存
        base_image.save(self.output_path)
        base_image.show()


# ----------------------------------------------------------------------------------

# **********************************************************************************


if __name__ == "__main__":
    debugMode = True
    # ベース画像のパスを指定
    base_image_path = "/Users/nyanyacyan/Desktop/Project_file/ImageAutomation/installer/src/method/inputData/A.png"
    output_path = "guide_lines.png"

    # ガイド線の範囲を指定 (左上x, 左上y, 右下x, 右下y)
    # ここで指定した範囲を枠線確認
    guide_boxes = [
        (0, 83, 1080, 998),
        (650, 93, 1050, 173),
        (50, 880, 550, 970),
        (700, 880, 1050, 970),
        (0, 850, 1200, 1080),
    ]

    # ガイド線を描画する
    guide_drawer = ImageGuideDrawer(base_image_path, output_path, debugMode)
    guide_drawer.draw_guides(guide_boxes)

# ----------------------------------------------------------------------------------


