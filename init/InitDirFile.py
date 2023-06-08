import base64
import os.path

from oem.oem_config import common_config
from setting.GLOBAL import DIR_LIST, FILE_LIST, ACTIVE_OEM_PATH, UPDATE_DOC_PATH


class InitDirFile:
    def __init__(self):
        self.create_dirs()
        self.create_files()
        self.create_update_log_file()

    def create_dirs(self):
        for item in DIR_LIST:
            if not os.path.exists(item):
                os.mkdir(item)

    def create_files(self):
        for item in FILE_LIST:
            if not item.exists():
                with item.open('a', encoding='utf-8') as f:
                    pass

    # 创建更新日志文件
    @staticmethod
    def create_update_log_file():

        with UPDATE_DOC_PATH.open('w', encoding='utf-8') as f_input:
            f_input.write(f'{common_config.welcome}\n\n当前版本：' + common_config.version + '\n\n')
            f_input.write("===========================================================================\n\n")
            for _, value in common_config.update.items():
                f_input.write(value)
                f_input.write("\n\n===========================================================================\n\n")

    @staticmethod
    def init_ico():
        img = ACTIVE_OEM_PATH / "title_ico.ico"
        picture = open("title_ico.ico", "wb+")
        picture.write(base64.b64decode(img))
        picture.close()
