# Encoding: UTF-8
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from db.init_data import init_base_config
from setting.GLOBAL import OEM_NAME
from db.models import Base, BasicConfig


class SqliteDB:
    def __init__(self, db_name):
        self.engine = create_engine(f'sqlite:///{db_name}.db')
        self.Session = sessionmaker(bind=self.engine)

        self.create_table()
        self.init_basic_config_table()

    def create_table(self):
        Base.metadata.create_all(self.engine)

    def drop_table(self):
        Base.metadata.drop_all(self.engine)

    def delete_table_info(self, table_name):
        """
        删除表中数据
        """
        session = self.Session()
        session.query(table_name).delete()
        session.commit()
        session.close()

    def init_basic_config_table(self):
        session = self.Session()
        basic_config = session.query(BasicConfig).all()
        if not basic_config:
            self.init_base_config(init_base_config)

    """
    基础设置操作模块
    """

    def init_base_config(self, base_config: BasicConfig):
        session = self.Session()
        session.add(base_config)
        session.commit()
        session.close()

    # 获取基础设置
    def get_base_config(self):
        session = self.Session()
        base_config = session.query(BasicConfig).first()
        session.close()
        return base_config

    # 更新基础设置
    def update_base_config(self,
                           proxy_file: str = None,
                           email_file: str = None,
                           two_fa: str = None,
                           session_dir_path: str = None,
                           thread_amount: int = None,
                           ie_style: str = None
                           ):
        """
        更新基础设置

        :param email_file:
        :param proxy_file:
        :param two_fa:
        :param session_dir_path:
        :param thread_amount:
        :param ie_style:
        :return:
        """

        session = self.Session()
        base_config_db = session.query(BasicConfig).first()

        if proxy_file:
            base_config_db.proxy_file = proxy_file
        if email_file:
            base_config_db.email_file = email_file
        if two_fa:
            base_config_db.two_fa = two_fa
        if session_dir_path:
            base_config_db.session_dir_path = session_dir_path
        if thread_amount:
            base_config_db.thread_amount = thread_amount
        if ie_style:
            base_config_db.ie_style = ie_style

        session.commit()
        session.close()


db_controller = SqliteDB(db_name=OEM_NAME)
