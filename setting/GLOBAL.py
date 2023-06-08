import os
from datetime import datetime
from pathlib import Path

OEM_NAME = "youmi"

BASE_DIR_PATH = Path.cwd()
BASE_PATH = str(os.getcwd())
BASE_OEM_PATH = BASE_DIR_PATH / "oem"
ACTIVE_OEM_PATH = BASE_OEM_PATH / OEM_NAME

HELP_DOC_PATH = BASE_DIR_PATH / "安装说明.txt"
UPDATE_DOC_PATH = BASE_DIR_PATH / "更新日志.txt"

# region keys文件夹相关设置
KEY_DIR = BASE_DIR_PATH / "Keys"
SECRET_FILE = KEY_DIR / "激活码.txt"

# endregion


# region 账号分类
ACCOUNT_DIR = BASE_DIR_PATH / "账号分类"
SUCCESS_ACCOUNT_FILE = ACCOUNT_DIR / "成功的账号.txt"
FAILED_ACCOUNT_FILE = ACCOUNT_DIR / "失败的账号.txt"

"""
session文件夹初始化
"""
# SESSION_DIR = BASE_PATH + "\\分类\\"
# DONE_DIR = BASE_PATH + "\\转换完成\\"
# FAILED_DIR = BASE_PATH + "\\转换失败\\"

"""
代理池
"""
PROXY_FILE = BASE_DIR_PATH / "代理池.txt"

EMAIL_FILE = BASE_DIR_PATH / "邮箱名.txt"

CHROME_PATH = r'C:\Program Files\Google\Chrome\Application\chromedriver.exe'  # C:\Program Files\Google\Chrome\Application\chromedriver.exe

"""
# LOG模块  log文件夹初始化
"""
# LOG_DIR = BASE_PATH + "\\Log\\"
DEV_LOG_DIR = BASE_DIR_PATH / "Log"
NOW_DATE = datetime.now().strftime("%Y%m%d%H%M%S")
LOG_FILE = DEV_LOG_DIR / f"{NOW_DATE}.log"

DEV_LOG_MODEL = 1
IS_SAVE_LOG = 1

DIR_LIST = [
     DEV_LOG_DIR,  KEY_DIR ,ACCOUNT_DIR
]

FILE_LIST = [
    PROXY_FILE, EMAIL_FILE, SECRET_FILE ,SUCCESS_ACCOUNT_FILE, FAILED_ACCOUNT_FILE
]
