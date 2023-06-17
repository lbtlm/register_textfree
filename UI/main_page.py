import asyncio
import random
import re
import urllib
from pathlib import Path
import threading
import time
from tkinter import PhotoImage
from tkinter.filedialog import askopenfilename
import ttkbootstrap as ttk
import urllib3
from playwright.async_api import async_playwright, Playwright

from UI.solve_captcha import SolveCaptcha
from playwright_recaptcha import recaptchav2

from playwright_recaptcha.errors import (
    RecaptchaNotFoundError,
    RecaptchaRateLimitError,
    RecaptchaSolveError,
)

from ttkbootstrap.constants import *
from ttkbootstrap.scrolled import ScrolledText
from ttkbootstrap.tooltip import ToolTip

from oem.oem_imgs.images_base import oem_image_dic
from setting.GLOBAL import LOG_FILE, OEM_NAME, BASE_DIR_PATH, SUCCESS_ACCOUNT_FILE, FAILED_ACCOUNT_FILE
from utils.COMMON_UTILS import common_utils
from utils.LogUtil import logger

from db.db_control import db_controller


class SubscribePremium(ttk.Frame):
    # +15878843622.session
    def __init__(self, master, overtime=None):
        super().__init__(master, padding=15)
        # self.card_path_var = "请选择信用卡txt，格式请见提示"  ttk.StringVar(value="abc123456")
        self.card_list = None
        self.over_time = overtime
        self.base_config = db_controller.get_base_config()

        self.two_fa_var = ttk.StringVar(value=self.base_config.two_fa)
        self.proxy_file_path_var = ttk.StringVar(value=self.base_config.proxy_file)
        self.email_path_var = ttk.StringVar(value=self.base_config.email_file)
        self.thread_var = ttk.StringVar(value=str(self.base_config.thread_amount))
        self.ie_select_var = ttk.StringVar(value=self.base_config.ie_style)

        self.code_dict = {}
        self.master = master

        self.failed = 0
        self.suc = 0
        self.amount = None
        self.complete = 0
        self.process_bar_value = 0
        self.loop = None
        self.log_frame = None
        self.log = None

        self.lock = threading.Lock()

        self.pack(fill="both", expand=True)

        logo_ico = PhotoImage(data=oem_image_dic[f'{OEM_NAME}_icon'])
        self.master.iconphoto(False, logo_ico)

        # application variables
        # _path = Path().absolute().as_posix()
        # self.path_var = ttk.StringVar(value=_path)

        # self.proxy_path_var = ttk.StringVar(value=self.proxy_file_path_var)

        self.row = ttk.Frame(self)
        self.row.pack(fill=X, expand=YES)

        # header and labelframe option container
        option_text = "配置栏"
        self.option_lf = ttk.Labelframe(self.row, text=option_text)
        self.option_lf.pack(fill=Y, expand=YES,
                            side=LEFT, padx=5, pady=5)

        self.create_path_row()
        self.create_results_view()

        process_frame = ttk.Frame(self)
        process_frame.pack(padx=5, fill=X, expand=YES)

        self.progressbar = ttk.Progressbar(
            master=process_frame,
            bootstyle=("success"),
            value=self.process_bar_value
        )
        self.progressbar.pack(side=LEFT, fill=X, expand=YES)

        self.pb_label = ttk.Label(
            master=process_frame,
            text=f'总完成: {self.process_bar_value}%',
            anchor=W,
            compound=CENTER)
        self.pb_label.pack(side=RIGHT)

        self.suc_label = ttk.Label(
            master=process_frame,
            text=f'成功: {self.suc}',
            anchor=W,
            compound=CENTER)
        self.suc_label.pack(side=RIGHT, padx=5)

        self.fail_label = ttk.Label(
            master=process_frame,
            text=f'失败: {self.failed}',
            anchor=W,
            compound=CENTER)
        self.fail_label.pack(side=RIGHT)

    def create_path_row(self):
        """Add path row to labelframe"""
        path_row_ads = ttk.Frame(self.option_lf)
        path_row_ads.pack(fill=X, side=TOP, pady=10)

        two_fa_lbl = ttk.Label(path_row_ads, text="请输入默认密码", width=20)
        ToolTip(two_fa_lbl, text="必填项，必须包含大小写字母和数字和特殊符号，长度为8-16位",
                bootstyle=("info", "inverse"))
        two_fa_lbl.pack(side=LEFT, padx=(10, 0))

        # self.two_fa = ttk.StringVar(value="abc123456")

        two_fa_ent = ttk.Entry(path_row_ads, textvariable=self.two_fa_var)
        two_fa_ent.pack(side=LEFT, fill=X, expand=YES, padx=10)

        # path_proxy_entry = ttk.Entry(path_row_ads, textvariable=self.proxy_path_var)
        # path_proxy_entry.pack(side=LEFT, fill=X, expand=YES, padx=5)

        path_proxy_row = ttk.Frame(self.option_lf)
        path_proxy_row.pack(fill=X, side=TOP, pady=10)

        path_proxy_lbl = ttk.Label(path_proxy_row, text="请选择代理文件夹", width=20)
        ToolTip(path_proxy_lbl,
                text="仅支持 http或https 协议代理池！！！开会员必须选择代理池，代理池的格式为 ： username:password@ip:port  \n例如:youmitools:youmipwd@192.168.1.20:7856",
                bootstyle=("info", "inverse"))
        path_proxy_lbl.pack(side=LEFT, padx=(10, 0))

        path_proxy_entry = ttk.Entry(path_proxy_row, textvariable=self.proxy_file_path_var)
        path_proxy_entry.pack(side=LEFT, fill=X, expand=YES, padx=(10, 0))

        proxy_btn = ttk.Button(
            master=path_proxy_row,
            text="选择",
            command=self.on_browse_proxy,
            width=8
        )
        proxy_btn.pack(side=LEFT, padx=(5, 10))

        # region 选择email文件
        path_row_cc = ttk.Frame(self.option_lf)
        path_row_cc.pack(fill=X, side=TOP, pady=10)

        path_lbl = ttk.Label(path_row_cc, text="请选择邮箱文件", width=20)
        path_lbl.pack(side=LEFT, padx=(10, 0))
        ToolTip(path_lbl, text="一行一个，默认格式为：dsf23432@gmail.com",
                bootstyle=("info", "inverse"))

        path_ent = ttk.Entry(path_row_cc, textvariable=self.email_path_var)
        path_ent.pack(side=LEFT, fill=X, expand=YES, padx=(10, 0))
        browse_btn = ttk.Button(
            master=path_row_cc,
            text="选择",
            command=self.on_browse_cc,
            width=8
        )
        browse_btn.pack(side=LEFT, padx=(5, 10))

        # endregion

        # region 线程数
        path_row_thread = ttk.Frame(self.option_lf)
        path_row_thread.pack(fill=X, side=TOP, pady=10)

        path_thread = ttk.Label(path_row_thread, text="请填入线程数", width=20)
        path_thread.pack(side=LEFT, padx=(10, 0))
        ToolTip(path_thread, text="请填入线程数，填入N，表示N个账号一起开会员，不建议填入太大，建议填入5",
                bootstyle=("info", "inverse"))

        path_ent = ttk.Entry(path_row_thread, textvariable=self.thread_var)
        path_ent.pack(fill=X, expand=YES, padx=10)

        # endregion

        # region 请选择浏览器种类
        path_row_ie = ttk.Frame(self.option_lf)
        path_row_ie.pack(fill=X, side=TOP, pady=10)

        path_ie = ttk.Label(path_row_ie, text="请选择浏览器种类", width=20)
        path_ie.pack(side=LEFT, padx=(10, 0))
        ToolTip(path_ie, text="目前仅支持火狐，谷歌浏览器。备注：由于火狐浏览器限制，只能单线程操作，谷歌浏览器可以多线程开会员",
                bootstyle=("info", "inverse"))

        self.ie_select = ttk.Combobox(path_row_ie, values=["谷歌浏览器", "火狐浏览器"], state="readonly")
        self.ie_select.pack(fill=X, expand=YES, padx=10)

        if self.base_config.ie_style == "火狐浏览器":
            self.ie_select.current(1)
        else:
            self.ie_select.current(0)

        # self.ie_select.current(0)

        # endregion

        # region 开始订阅 取消任务

        path_row_button = ttk.Frame(self.option_lf)
        path_row_button.pack(fill=X, side=TOP, pady=10)

        start_btn = ttk.Button(
            master=path_row_button,
            text="开始订阅",
            command=self.run_new,
        )
        start_btn.pack(side=LEFT, padx=(10, 5), fill=X, expand=YES)

        cancel_btn = ttk.Button(
            master=path_row_button,
            text="取消任务",
            command=self.cancel,
        )
        cancel_btn.pack(side=LEFT, padx=(5, 10), fill=X, expand=YES)
        # endregion

    def create_results_view(self):
        self.log = ScrolledText(self.row)
        self.log.pack(fill=BOTH, expand=YES, pady=5, side=RIGHT, padx=5)
        # self.tg_common = TG_COMMON(log=self.log)

    # def on_browse(self):
    #     """Callback for directory browse"""
    #     path = askdirectory(title="请选择session文件夹", initialdir=BASE_DIR_PATH)
    #     if path:
    #         self.session_file_path_var.set(path)

    def on_browse_cc(self):
        """Callback for directory browse"""
        path = askopenfilename(title="请选择信用卡文件", initialdir=BASE_DIR_PATH)
        if path:
            self.email_path_var.set(path)

    def on_browse_proxy(self):
        """Callback for directory browse"""
        path = askopenfilename(title="请选择代理文件", initialdir=BASE_DIR_PATH)
        if path:
            self.proxy_file_path_var.set(path)

    def insert_log(self, text: str):
        log_text = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()) + "--" + text + '\n'
        self.log.insert(END, log_text)
        self.log.see(END)
        logger.info(text)
        common_utils.insert_log(LOG_FILE, log_text)

    # region 优化线程入口
    def run_new(self):
        # 更新数据库 配置

        print(self.ie_select.get())

        db_controller.update_base_config(
            proxy_file=self.proxy_file_path_var.get(),
            email_file=self.email_path_var.get(),
            two_fa=self.two_fa_var.get(),
            thread_amount=int(self.thread_var.get()),
            ie_style=self.ie_select.get(),
        )

        # self.email_list = common_utils.convert_card_file_to_list(file=self.email_path_var.get())

        # 获取全部参数
        # session_dir = self.session_file_path_var.get()
        email_file_path = self.email_path_var.get()
        if not Path(email_file_path).exists():
            self.insert_log('邮件文件不存在，请检查！')
            return

        proxy_file_path = self.proxy_file_path_var.get()

        if not Path(proxy_file_path).exists():
            self.insert_log('代理文件不存在，请检查！')
            return

        # 获取所有session文件
        email_files_list = common_utils.get_all_email(Path(email_file_path))

        self.amount = len(email_files_list)

        # 获取线程数
        thread_num = int(self.thread_var.get())
        sem = threading.Semaphore(thread_num)

        # 空session文件夹
        if not email_files_list:
            self.insert_log('邮件文件为空！')
        else:
            tasks_num = len(email_files_list)

            # threads = []
            for num in range(thread_num):
                t = threading.Thread(target=self.start_new, args=(sem,))
                t.daemon = True
                t.start()

    # endregion

    def start_new(self, sem: threading.Semaphore):
        with sem:
            try:
                loop = asyncio.new_event_loop()
                loop.run_until_complete(self.register_textfree())
            except asyncio.CancelledError as cancel_error:
                print(f"loop被强制取消，触发取消错误：{cancel_error}")

            except Exception as error:
                print(f"触发其他错误：{error}")
            finally:
                print(f"loop关闭")
                loop.close()

    def cancel(self):

        # 关闭所有线程
        for thread in threading.enumerate():
            if thread != threading.current_thread() and thread.name != "check_beat":
                print(thread.ident, thread.name)

                thread.join(1)

        self.insert_log(f"所有任务已取消！")

    def change_process_bar_frame(
            self,
            process_bar_value: int = None,
    ):
        if process_bar_value:
            self.process_bar_value = process_bar_value

        self.fail_label.configure(text=f'失败: {self.failed}')
        self.suc_label.configure(text=f'成功: {self.suc}')
        self.progressbar.configure(value=self.process_bar_value)
        self.pb_label.configure(text=f'完成: {self.process_bar_value}%')

    async def register_textfree(self):

        task_register_textfree = asyncio.create_task(self.register_textfree_ie())

        done, pending = await asyncio.wait([task_register_textfree])
        for task in done:
            # logger.info(f"任务 {task.get_name()} 执行完毕！结果为：{task.result()}")

            print(f"任务 {task.get_name()} 执行完毕！结果为：{task.result()}")

    async def register_textfree_ie(self):
        # return
        # phone_number = Path(session_file).stem
        failed_times = 0
        while True:
            email = common_utils.get_and_del_first_line(Path(self.email_path_var.get()))

            if email == "":
                # self.insert_log("邮箱文件已经全部使用完毕！")
                failed_times += 1
                if failed_times >= 5:
                    self.insert_log("邮箱文件已经全部使用完毕！")
                    break

                await asyncio.sleep(0.1)

            else:
                failed_times = 0

                # return
                async with async_playwright() as playwright:
                    # json_file = Path(session_file).parent / f"{Path(session_file).stem}.json"
                    subscribe_premium_res = await self.do_register_textfree(playwright=playwright, email=email)
                    print(subscribe_premium_res)

                    # json_file = Path(session_file).parent / f"{Path(session_file).stem}.json"

                    if subscribe_premium_res is True:
                        common_utils.insert_txt_line(file=SUCCESS_ACCOUNT_FILE, text=email)
                        self.suc += 1
                    else:
                        common_utils.insert_txt_line(file=FAILED_ACCOUNT_FILE, text=email)
                        self.failed += 1

                self.complete += 1
                self.change_process_bar_frame(int(self.complete * 100 / self.amount))

    async def do_register_textfree(self, playwright: Playwright, email: str) -> bool:

        args = [
            '--deny-permission-prompts',
            '--no-default-browser-check',
            '--no-first-run',
            '--deny-permission-prompts',
            '--disable-popup-blocking',
            '--ignore-certificate-errors',
            '--no-service-autorun',
            '--password-store=basic',
            '--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.212 Safari/537.36',
            '--disable-audio-output'
        ]

        try:
            # 进入循环  获取代理池
            proxy_failed_times = 0
            # proxy_none_times = 0
            while True:
                proxy = common_utils.get_first_line_proxy(file=self.proxy_file_path_var.get(), lock=self.lock)
                if proxy == {}:
                    self.insert_log(f"账号 {email} 获取代理池为空，结束任务！")
                    return False

                # 获取浏览器种类
                browser_type = self.ie_select.current()
                if browser_type == 1:

                    browser = await playwright.firefox.launch(headless=False,  # http://70.kookeey.info:11988
                                                              proxy=proxy,
                                                              args=args
                                                              )
                else:
                    browser = await playwright.chromium.launch(headless=False,  # 70.kookeey.info:11988
                                                               proxy=proxy,
                                                               args=args,
                                                               chromium_sandbox=True
                                                               )

                page = await browser.new_page()

                try:
                    self.insert_log(f"账号 {email} 正在进行浏览器注册...，使用代理 {proxy['server']}")
                    await page.goto("https://messages.textfree.us/register", timeout=60000)

                    break
                except Exception as e:
                    print(e)
                    self.insert_log(f"账号 {email} 代理 {proxy['server']} 60秒无法加载页面，正在更换代理...")
                    await browser.close()
                    proxy_failed_times += 1
                    if proxy_failed_times >= 5:
                        self.insert_log(f"账号 {email} 更换代理次数过多，放弃此账号...")
                        return False

                    await asyncio.sleep(3)
                    continue

            await page.get_by_placeholder("Email").fill(email, timeout=30000)
            self.insert_log(f"账号 {email} 成功输入邮箱名...")
            await page.wait_for_timeout(3000)

            two_fa = self.two_fa_var.get()
            await page.get_by_placeholder("Password", exact=True).fill(two_fa, timeout=30000)
            self.insert_log(f"账号 {email} 成功输入密码...")
            await page.wait_for_timeout(3000)

            await page.get_by_placeholder("Confirm Password", exact=True).fill(two_fa, timeout=30000)
            self.insert_log(f"账号 {email} 成功输入确认密码...")
            await page.wait_for_timeout(3000)

            # 新版 captche
            try:
                captcha_solver = SolveCaptcha(page,email)
                solver_res = await captcha_solver.start()
                if solver_res is False:
                    self.insert_log(f"账号 {email} 人机验证失败.")
                    del captcha_solver
                    return False
                else:
                    self.insert_log(f"账号 {email} 人机验证成功.")
                    del captcha_solver

            except Exception as e:
                print(f"人机验证失败，触发错误{e}")
                self.insert_log(f"账号 {email} 人机验证失败.")
                # await browser.close()
                return False

            # solver_failed_times = 0
            # async with recaptchav2.AsyncSolver(page) as solver:
            #     self.insert_log(f"账号 {email} 开始人机验证...")
            #     while True:
            #         try:
            #             token = await solver.solve_recaptcha()
            #             print(token)
            #             self.insert_log(f"账号 {email} 人机验证成功")
            #             break
            #         except RecaptchaNotFoundError:
            #             solver_failed_times += 1
            #             if solver_failed_times >= 3:
            #                 self.insert_log(f"账号 {email} 连续3次未检测到人机验证框，直接退出...")
            #                 return False
            #             self.insert_log(f"账号 {email} 未检测到人机验证框，休息3秒，再次检测...")
            #             await asyncio.sleep(3)
            #             continue
            #         except RecaptchaRateLimitError:
            #             self.insert_log(f"账号 {email} 人机验证频率过快，直接退出...")
            #             return False
            #         except RecaptchaSolveError:
            #             solver_failed_times += 1
            #             if solver_failed_times >= 3:
            #                 self.insert_log(f"账号 {email} 连续3次人机验证无法处理，直接退出...")
            #                 return False
            #             self.insert_log(f"账号 {email} 人机验证无法处理，休息3秒，再次检测...")
            #             await asyncio.sleep(3)
            #             continue
            #         except Exception as error:
            #             print(error)
            #             self.insert_log(f"账号 {email} 人机验证触发未知错误，直接返回...\n{error}")
            #             return False
            try:
                await page.get_by_role("button", name="Sign Up", exact=True).click(timeout=30000)
                self.insert_log(f"账号 {email} 点击注册按钮成功")
            except Exception as e:
                print(e)
                self.insert_log(f"账号 {email} 点击注册按钮失败，直接返回...")
                return False

            try:
                await page.get_by_role("button", name="Got it").click(timeout=30000)
                self.insert_log(f"账号 {email} 检测点击注册跳转成功")
            except Exception as e:
                print(e)
                self.insert_log(f"账号 {email} 检测点击注册跳转失败，直接返回...")
                return False

            try:

                await page.get_by_text("Choose a TextFree Number").click(timeout=120000)
                self.insert_log(f"账号 {email} 检测到选择号码页面，注册成功")
            except Exception as e:
                print(e)
                self.insert_log(f"账号 {email} 120秒内，未检测到选择号码页面，直接返回...")
                return False

            return True
        except Exception as e:
            self.insert_log(f"账号 {email} 注册失败，原因：{e}")
            return False
