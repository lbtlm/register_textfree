import logging
import os
import time
from logging import handlers

from setting.GLOBAL import DEV_LOG_DIR, DEV_LOG_MODEL, IS_SAVE_LOG, LOG_FILE


class Logger(object):
    def __init__(self, logger_name, is_save_file):
        """
        定义保存日志的文件路径，日志级别，以及调用文件
        将日志存入指定文件中
        将日志输出到控制台中
        :param logger_name:str
        """
        self.is_save_file = is_save_file

        # 1、创建一个logger
        self.logger = logging.getLogger(logger_name)  # 返回一个logger实例
        self.logger.setLevel(logging.DEBUG)  # 设置logger级别为debug

        # 2、再创建yig handler，用于输出到控制台
        ch = logging.StreamHandler()
        ch.setLevel(logging.INFO)

        # 3、定义handler的输出格式
        # formatter = logging.Formatter('%(asctime)s - %(filename)s[line:%(lineno)d] - %(levelname)s : %(message)s')
        if DEV_LOG_MODEL == 1:
            formatter = logging.Formatter(f'%(asctime)s - %(filename)s[line:%(lineno)d] - %(levelname)s  : %(message)s', "%Y-%m-%d %H:%M:%S")
        else:
            formatter = logging.Formatter(f'%(asctime)s -  %(levelname)s  : %(message)s', "%Y-%m-%d %H:%M:%S")
        ch.setFormatter(formatter)

        # 4、将logger添加到handler里面   判断如果是开发模式 ，就新建DevLog文件夹，及开发模式log文件
        if self.is_save_file == 1:
            if not os.path.exists(DEV_LOG_DIR):
                os.mkdir(DEV_LOG_DIR)
            else:
                # 限制log文件夹下只有10个最近的日志文件，防止日志文件过多占用内存
                num = 0
                item_list = list(DEV_LOG_DIR.rglob('*.log'))
                for item in item_list:
                    num += 1
                    if num >= 10:
                        item_list[0].unlink()

            # 5、 创建一个handler,用于写入日志文件
            rq = time.strftime('%Y%m%d%H%M%S', time.localtime(time.time()))
            log_name = DEV_LOG_DIR / (rq + '.log')
            # fh = logging.FileHandler(log_name, mode='w')
            fh = handlers.TimedRotatingFileHandler(filename=log_name, encoding="utf-8")
            fh.setFormatter(formatter)
            fh.setLevel(logging.INFO)
            self.logger.addHandler(fh)
        self.logger.addHandler(ch)

    def get_log(self):
        return self.logger


log = Logger("register_dev", IS_SAVE_LOG)
logger = log.get_log()
