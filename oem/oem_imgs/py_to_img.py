import base64

from UI.imgs.images_base import image_dic
from setting.GLOBAL import PICS_DIR


class Images:
    def __init__(self):
        self.py_to_pics()

    def py_to_pics(self):
        for key ,value in image_dic.items():
            tmp = open(f"{PICS_DIR}{key}.png", "wb+")
            tmp.write(base64.b64decode(value))
            tmp.close()

    def remove_pics(self):

        pass

