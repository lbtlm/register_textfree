import importlib

from setting.GLOBAL import OEM_NAME


class CommonConfig:
    def __init__(self, oem_name: str):

        self.config_oem_name = importlib.import_module(f'oem.{oem_name}')

        self.about = self.config_oem_name.config.about
        self.title = self.config_oem_name.config.title
        self.welcome = self.config_oem_name.config.welcome
        self.doc = self.config_oem_name.config.doc

        self.icon = self.config_oem_name.config.icon
        self.update = self.config_oem_name.config.update
        self.name = self.config_oem_name.config.name

        self.app_code = self.config_oem_name.config.app_code
        self.app_version = self.config_oem_name.config.app_version
        self.version = self.config_oem_name.config.version


common_config = CommonConfig(OEM_NAME)
