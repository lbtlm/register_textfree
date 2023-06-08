from oem.oem_imgs.images_base import oem_image_dic

from setting.GLOBAL import OEM_NAME, BASE_DIR_PATH

help_doc = "写在前面：\n\n" \
           "首先，必须确保自己电脑是真全局VPN，因为kookeey代理池禁止国内访问，具体请参考一下两篇文章 ,强调：V2RAY不是真全局！！！" \
           "\n1.怎么判断自己网络是不是——真·全局环境  https://youmitools.com/?p=309" \
           "\n2.CLASH FOR WINDOWS 设置真全局模式（TUN模式） https://youmitools.com/?p=349" \
           "\n3.LETSVPN（快连）设置全局网络教程  https://youmitools.com/?p=341" \
           "\n\n安装教程：" \
           "\n1.KOOKEEY代理池设置:https://youmitools.com/?p=494" \
           "\n2.TG注册机其他配置教程 https://youmitools.com/?p=497" \
           "\n3.TG注册机使用教程 https://youmitools.com/?p=501" \
           "\n\n如果还有其他疑问，请联系客服：@youmi_kefu"

update_dict = {
    "0.0.9": "0.0.9 更新日志：\n\n更新日期：2023-6-5\n1.修复N个账号，每个账号都是不同二级密码，优先读取json中twoFA字段，如没有，则读取通用二级密码\n2.修复日志问题\n3.修复UI界面",
    "0.0.8": "0.0.8 更新日志：\n\n更新日期：2023-5-31\n1.修复多线程获取代理池错误\n2.修复多线程获取卡号错误\n3.修复loop异常关闭错误\n4.修复tg_client为bool或者为str错误\n5.修复其他已知错误",
    "0.0.7": "0.0.7 更新日志：\n\n更新日期：2023-5-24\n1.修复代理池无法使用，重复5次\n2.修复信用卡读取次数，加减方式\n3.修复多语言匹配\n4.修复进度条显示错误\n5.修复成功失败，转移文件报错\n6.增加数据库记忆功能\n7.多协程改为多进程操作"
}


class Config:
    def __init__(self):
        self.name = "纸飞机"
        self.customer = ""
        self.version = "0.0.9"
        self.about = "有米工具箱 专注于开发各种营销类软件\n唯一TG客服 @youmi_kefu\n官方网站：www.youmitools.com"
        self.title = f"请联系客服 获取激活码"
        self.welcome = "纸飞机TG批量开会员助理"
        self.doc = help_doc
        self.update = update_dict
        self.icon = oem_image_dic[f"{OEM_NAME}_icon"]
        self.app_code = "9703feae038b11ee9b2f00bf3ea3203c"
        self.app_version = "1.0.0.1"


config = Config()
