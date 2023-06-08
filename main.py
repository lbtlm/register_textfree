import multiprocessing
import sys
import threading
from tkinter import messagebox

from UI.login_page import LoginPage
from init.InitDirFile import InitDirFile
from oem.oem_config import common_config

from ttkbootstrap.window import Window


def on_closing():
    if messagebox.askokcancel("退出软件", "确定退出软件吗？"):
        # 关闭所有线程
        for thread in threading.enumerate():
            if thread != threading.current_thread():
                print(thread.ident, thread.name)
                thread.join(1)

        # 关闭所有进程
        for process in multiprocessing.active_children():
            print(process.pid, process.name)
            process.terminate()
            process.join(1)

        PLAYWRIGHT_BROWSERS_PATH = 0
        app.destroy()

        app.quit()
        # 结束程序

        sys.exit()
        #
        # 2.0 beta版本
        # 自动退出进程 及线程


if __name__ == '__main__':
    InitDirFile()
    app = Window(common_config.title, themename="cosmo")
    app.protocol("WM_DELETE_WINDOW", on_closing)
    LoginPage(app)
    app.mainloop()
