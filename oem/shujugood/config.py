from oem.oem_imgs.images_base import oem_image_dic

from setting.GLOBAL import OEM_NAME, BASE_DIR_PATH

help_doc = ""

update_dict = {
}


class Config:
    def __init__(self):
        self.name = "数据谷TG批量开会员助理"
        self.customer = ""
        self.version = "0.0.9"
        self.about = "有米工具箱 专注于开发各种营销类软件\n唯一TG客服 @youmi_kefu\n官方网站：www.youmitools.com"
        self.title = f"版本号({self.version}) 软件路径：{str(BASE_DIR_PATH)}"
        self.welcome = "数据谷TG批量开会员助理"
        self.doc = help_doc
        self.update = update_dict
        self.icon = oem_image_dic[f"{OEM_NAME}_icon"]
        self.app_code = "8ee96244038b11ee9b2f00bf3ea3203c"
        self.app_version = "1.0.0.1"


config = Config()
