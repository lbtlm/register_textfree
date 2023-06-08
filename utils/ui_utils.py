# coding:utf-8
import base64
import tkinter as tk
from io import BytesIO

from PIL import Image, ImageTk


# noinspection PyMethodMayBeStatic
class UICommonUtils:

    # 窗口居中 ，mac windows通用
    def center_window(self, win, width=None, height=None):
        """ 将窗口居中 """
        screenwidth = win.winfo_screenwidth()
        screenheight = win.winfo_screenheight()
        if width is None:
            # width = int(screenwidth / 2)
            # height = int(screenheight / 2)
            width = 1440
            height = 900

        size = '%dx%d+%d+%d' % (width, height, (screenwidth - width) / 2, (screenheight - height) / 3)
        win.minsize(width, height)
        win.geometry(size)

    # noinspection PyMethodMayBeStatic
    def get_window_size(self, win, update=True):
        """ 获得窗体的尺寸 """
        if update:
            win.update()
        return win.winfo_width(), win.winfo_height(), win.winfo_x(), win.winfo_y()

    # noinspection PyMethodMayBeStatic
    def tkimg_resized(self, img, w_box, h_box, keep_ratio=True):
        """对图片进行按比例缩放处理"""
        width = 0
        height = 0
        w, h = img.size

        if keep_ratio:
            if w > h:
                width = w_box
                height = int(h_box * (1.0 * h / w))

            if h >= w:
                height = h_box
                width = int(w_box * (1.0 * w / h))
        else:
            width = w_box
            height = h_box

        img1 = img.resize((width, height), Image.LANCZOS)
        tkimg = ImageTk.PhotoImage(img1)
        return tkimg

    def set_icon_win(self, img):
        icon_img = base64.b64decode(img)
        icon_img = ImageTk.PhotoImage(data=icon_img)

        return icon_img

    def image_label(self, frame, img, width, height, keep_ratio=True):
        """输入图片信息，及尺寸，返回界面组件"""

        if isinstance(img, str):
            b64_de_img = base64.b64decode(img)  # base64解码
            b_io_img = BytesIO(b64_de_img)
            # img = Image.open(b_io_img)
            _img = Image.open(b_io_img)
        else:
            _img = img
        lbl_image = tk.Label(frame, width=width, height=height)

        tk_img = self.tkimg_resized(_img, width, height, keep_ratio)
        lbl_image.image = tk_img
        lbl_image.config(image=tk_img)
        return lbl_image


ui_common_utils = UICommonUtils()
