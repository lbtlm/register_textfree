import json
import time
import uuid
from threading import Thread
from tkinter import StringVar, PhotoImage
from tkinter.messagebox import showinfo

import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from UI.main_page import SubscribePremium
from utils.ui_utils import ui_common_utils
from db.db_control import db_controller
from setting.GLOBAL import SECRET_FILE, LOG_FILE
from utils.COMMON_UTILS import common_utils

from utils.LogUtil import logger
from oem.oem_config import common_config

g_machine_info = common_utils.get_machine_info()


class LoginPage(object):
    def __init__(self, master=None):
        self.cancel_btn = None
        self.login_btn = None
        self.btn_frame = None
        self.active_code_entry = None
        self.page = None
        self.root = master  # 定义内部变量root
        # ui_common_utils.center_window(self.root, width=400, height=300)

        logo_ico = PhotoImage(data=common_config.icon)
        self.root.iconphoto(False, logo_ico)
        # self.root.iconbitmap("logo.ico")
        # os.remove("logo.ico")
        self.password = StringVar()
        self.wtfcard_root_url = "https://card.youmitools.com/api/api-client/v1/app/" + common_config.app_code
        self.g_key = ""
        self.createPage()

    def createPage(self):
        # db_controller.shutdown()
        # db_controller.startup()

        self.page = ttk.Frame(self.root)  # 创建Frame
        self.page.pack(pady=60, anchor="center")
        ttk.Label(self.page, text=common_config.welcome, font=('', 14, 'bold'), anchor="center").pack(side=TOP, fill=X)
        ttk.Label(self.page, text=common_config.version, font=('microsoft yahei', 12), anchor="center").pack(side=TOP, fill=X, pady=(8, 0))
        self.active_code_entry = ttk.Entry(self.page, width=30, show="*")
        self.insert_secret_code()
        self.active_code_entry.pack(side=TOP, fill=X, pady=20, padx=5)

        self.btn_frame = ttk.Frame(self.page)
        self.btn_frame.pack(side=TOP, fill=X)

        self.login_btn = ttk.Button(
            master=self.btn_frame,
            text='登录',
            compound=CENTER,
            command=self.on_click_sign_in,
            bootstyle=PRIMARY
        )
        self.login_btn.pack(side=LEFT, fill=BOTH, expand=YES, padx=5)

        self.cancel_btn = ttk.Button(
            master=self.btn_frame,
            text='取消',
            compound=CENTER,
            command=self.page.quit,
            bootstyle=PRIMARY
        )
        self.cancel_btn.pack(side=RIGHT, fill=BOTH, expand=YES, padx=5)

        ui_common_utils.center_window(self.root, width=400, height=300)

    def insert_secret_code(self):
        with open(SECRET_FILE, 'r', encoding='utf-8') as f:
            code = f.read()
            if code != "":
                self.active_code_entry.insert(0, code)

    def insert_code_to_txt(self):
        with open(SECRET_FILE, 'w', encoding="utf-8") as f:
            code = self.active_code_entry.get().strip()
            f.write(code)

    def check_sign(self, dic):
        local_sign = ""
        sign_guid = "E08A38E3-DD98-4534-B91D-2C77F5FFA8DE"
        local_sign = sign_guid
        for i in sorted(dic):
            local_sign += "+" + str(dic[i])
        local_sign = common_utils.md5(local_sign)
        local_sign = common_utils.md5("{}{}".format(local_sign, sign_guid))
        return local_sign

    # 接收到卡密登录、心跳post请求的结果
    def handle_post_result(self, result, guid, is_sign_in=False):
        result_reader = json.loads(result)
        code = result_reader["code"]

        if code == 1:
            # print(result_reader)
            interval = result_reader["data"]["interval"]
            overtime = result_reader["data"]["overtime"]
            sign = result_reader["data"]["sign"]
            service_time = result_reader["data"]["time"]
            check_sign_dic = {"overTime": overtime, "machineCode": g_machine_info,
                              "magicCode": guid, "time": service_time, "version": common_config.app_version}
            local_sign = self.check_sign(check_sign_dic)
            # print('我的签名：' + local_sign)
            if local_sign == sign:
                if is_sign_in:
                    # self.tabControl.place(x=10, y=5, width=880, height=250)  # 登录成功，显示操作区域
                    # self.destroy()  # 等待直到login销毁，不销毁后面的语句就不执行
                    # app = MainWindow()
                    # index(app)
                    self.insert_code_to_txt()

                    login_success = "登录成功"
                    showinfo(message=login_success)
                    self.page.destroy()
                    # MainPage(self.root, overtime)
                    SubscribePremium(self.root, overtime)
                    ui_common_utils.center_window(self.root, width=1000, height=500)

                # self.set_wnd_title(overtime)
                return interval
            else:
                error_msg = "签名验证失败"
        else:
            error_msg = result_reader["msg"]
            if code == -21:  # 检测升级
                v_info = result_reader['data']['info']
                # v_down_url = "https://t.me/ruanjianxiazai1"
                v_down_url = result_reader['data']['downloadUrl']
                # v_version = v_info.split("\n")[0]
                v_version = result_reader['data']['version']
                logger.info('最新版本是：{} \n'.format(v_version))
                logger.info('你的版本是: {}\n'.format(common_config.app_version))
                logger.info('最新版本下载链接：{} \n'.format(v_down_url))
                logger.info('最新版本更新信息： \n{}'.format(v_info))
                v_message = '现在最新版本是：{} \n' \
                            '你的版本是: {}\n' \
                            '最新版本下载链接：{} \n' \
                            '最新版本更新信息： \n{}'.format(v_version, common_config.app_version, v_down_url, v_info)
                error_msg = error_msg + '\n' + v_message
                showinfo(message=error_msg)

                # logger.info(v_message)
                # if is_sign_in:
                #     top.destroy()  # error_msg,
            elif code == -30 or code == -31 or code == -32 or code == -33:
                # if not is_sign_in:
                user_no_exist = "无效的卡密!"
                self.active_code_entry.delete(0, END)
                showinfo(message=user_no_exist)
        # logger.info("服务器验证失败，code={}，error_msg={}".format(code, error_msg))
        return False

    # 点击卡密登录
    def on_click_sign_in(self):
        # 更新配置文件
        self.g_key = self.active_code_entry.get().strip()
        if self.g_key != "":
            guid = str(uuid.uuid1())
            root_url = "{}/bind".format(self.wtfcard_root_url)
            params = {"machineCode": g_machine_info, "reCode": self.g_key,
                      "magicCode": guid, "version": common_config.app_version}
            # logger.info('我的请求参数:' + str(params))
            try:
                result = common_utils.http_post(root_url, params)
                # print(result)  # 打印返回值
                if result == "":
                    # logger.info("网络错误，请检查网络")
                    showinfo(message="网络错误，请检查网络")
                    return
                interval = self.handle_post_result(result, guid, True)
                if interval is False:
                    return

                logger.info("登录成功")
                common_utils.insert_log(LOG_FILE, "登录成功")

                time.sleep(0.5)
                t = Thread(target=self.check_beat, name="check_beat")
                # t.setDaemon(True)
                t.daemon = True
                t.start()
            except Exception as e:
                print(str(e))
                logger.info("服务器返回信息异常，请检查网络，偶尔丢包属正常情况")
        else:
            login_none = "卡密不能为空"
            showinfo(message=login_none)

    # 心跳
    def check_beat(self):
        post_failed_times = 0
        while True:
            interval = 60
            guid = str(uuid.uuid1())
            root_url = "{}/beat".format(self.wtfcard_root_url)
            params = {"machineCode": g_machine_info, "reCode": self.g_key,
                      "magicCode": guid, "version": common_config.app_version}
            try:
                result = common_utils.http_post(root_url, params)
                # print(result)

                interval = self.handle_post_result(result, guid)
                # print("检测心跳结果: " + str(interval))
                if interval is False:
                    post_failed_times += 1
                    interval = 60
                else:
                    post_failed_times = 0
            except:
                # logger.info("心跳：服务器返回信息异常，请检查网络或联系作者")
                post_failed_times += 1
                if post_failed_times >= 6:
                    error_msg = "服务器返回信息异常次数超过限制"
                    # self.active_code_entry.delete(0, END)
                    # showinfo(message=error_msg)
            time.sleep(interval)
