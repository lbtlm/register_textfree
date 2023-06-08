from datetime import datetime
from sqlalchemy.orm import declarative_base
from sqlalchemy import Column, Integer, String, Boolean, TEXT, DateTime

Base = declarative_base()


class BasicConfig(Base):
    __tablename__ = 'basic_configs'

    iid = Column(Integer, primary_key=True, autoincrement=True, nullable=True, name="id")

    proxy_file = Column(String, nullable=True, default="", name="代理文件路径")
    email_file = Column(String, nullable=True, default="", name="邮箱文件路径")
    two_fa = Column(String, default="ABC123456!", name="密码")
    thread_amount = Column(Integer, default=0, name="线程数")
    ie_style = Column(String, default="谷歌浏览器", nullable=True, name="浏览器类型")





