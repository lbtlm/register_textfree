import fileinput
import hashlib
import random
import threading
import time
import uuid
from datetime import datetime
from pathlib import Path
from tkinter.messagebox import showerror
from typing import Union

import requests
import urllib3




class COMMON_UTILS:
    def __init__(self):
        pass

    # 新增一行数据
    def insert_txt_line(self, file: Path, text: str):
        value = text + "\n"
        with file.open('a', encoding='utf-8') as f:
            f.write(value)

    def insert_log(self, file: Path, text: str):
        with file.open('a', encoding='utf-8') as f:
            f.write(text)

    def del_txt_line(self, file: Path, text: str):

        try:

            line_value = text + "\n"
            with file.open('r', encoding='utf-8') as f_read:
                lines = f_read.readlines()

            lines.remove(line_value)

            with file.open('w', encoding='utf-8') as f_write:
                f_write.writelines(lines)

        except Exception as error:
            print(error)

    # 通过路径，获得手机号
    def get_phone_num(self, file_path: str) -> str:
        return Path(file_path).stem

    # 获取随机n个字母,返回字符串
    def get_random_set(self, bits):
        char_set = [chr(i) for i in range(97, 123)]
        res = "".join(random.sample(char_set, bits))
        return res

    def get_all_lines(self, file_path: Path) -> list:
        with Path.open(file_path, 'r', encoding='utf-8') as f:
            lines = f.readlines()
        return lines

    # 获取 txt文件夹下 随机一行
    def get_random_line(self, file_name: Path):
        with Path.open(file_name, 'r', encoding='utf-8') as f:
            lines = f.readlines()
        res = random.choice(lines).strip()
        return res

    def get_first_line(self, file_name: Path):
        with Path.open(file_name, 'r', encoding='utf-8') as f:
            lines = f.readlines()

        return lines[0].strip()

    def read_txt(self, file_name: Path):
        with Path.open(file_name, 'r', encoding='utf-8') as f:
            return f.read()

        # return lines[0].strip()

    def get_and_del_first_line(self, file_name: Path):
        try:
            text = ""
            for line in fileinput.input(file_name, openhook=fileinput.hook_encoded('utf-8')):
                if not fileinput.isfirstline():
                    line.replace("\n", "")
                else:
                    text = line.replace("\n", "")
            text.replace(" ", "")
            with open(file_name, 'r', encoding='utf-8') as r:
                lines = r.readlines()
            with open(file_name, 'w', encoding='utf-8') as w:
                del lines[0]
                for line in lines:
                    w.write(line)
        except:
            text = ""
        return text

    @staticmethod
    def get_now_time():
        return datetime.now().strftime('%Y%m%d%H%M%S')


    # region  md5加密
    @staticmethod
    def md5(text):
        h = hashlib.md5()
        h.update(text.encode("utf-8"))
        return h.hexdigest()

    # endregion

    # region  获取机器码
    def get_machine_info(self):
        # g_machine_info = ""
        g_uuid_tep = ""
        for i in range(5):
            g_uuid_tep += str(uuid.uuid1())
            # disk_id = self.get_disk_id()
            # cpu_id = self.get_cpu_id()
        g_machine_info = self.md5(f"{g_uuid_tep}")
        if g_machine_info != "":
            return g_machine_info
        if g_machine_info == "":
            showerror("错误", "获取机器码失败，请联系作者")

    # endregion

    # region  http请求卡密
    # 异步post请求，防止卡UI线程
    @staticmethod
    def http_post(url, params=None, timeout=30):
        urllib3.disable_warnings()
        header = {"Connection": "close"}
        res = ""
        failed_times = 0
        while res == "":
            try:
                res = requests.post(url, data=params, headers=header, timeout=timeout, verify=False)
                break
            except Exception as e:
                # print(e)
                failed_times += 1
                if failed_times == 5:
                    break
                time.sleep(2)
                continue

        if res == "":
            return res
        elif res.status_code == 200:
            result_text = res.text
            return result_text
        else:
            return ""

    # endregion

    # region  获取第一行代理池字典
    def get_first_line_proxy(self, file: str,lock:threading.Lock) -> dict:
        # 判断代理池文件格式
        with lock:
            proxy_line = common_utils.get_and_del_first_line(Path(file))
            if isinstance(proxy_line, str) and "@" in proxy_line:

                proxy_auth = proxy_line.split("@")[0]
                proxy_username = proxy_auth.split(":")[0]
                proxy_password = proxy_auth.split(":")[1]

                proxy_ip_port = proxy_line.split("@")[1]

                proxy = {
                    "server": "http://" + proxy_ip_port,
                    "username": proxy_username,
                    "password": proxy_password
                }

            else:
                proxy = {}

            return proxy

    # endregion


    # 获取所有邮箱列表
    def get_all_email(self, file: Path) -> list:
        with file.open('r', encoding='utf-8') as f:
            return f.readlines()

        # return lines

common_utils = COMMON_UTILS()

# if __name__ == '__main__':
#     common_utils.credit_card_times_add(file_path=CARD_FILE, card_number="5572710150806595")
