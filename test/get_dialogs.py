import asyncio

from telethon import TelegramClient

from utils.COMMON_UTILS import common_utils
from utils.tg_common import tg_common

session_file =  r'C:\Users\55049\PycharmProjects\subscribe_premium\sessions\8562076274459.session'

# random_api_id, random_api_hash, random_device_model, random_system_version, random_app_version, random_lang_pack = common_utils.get_random_developer_device_app(
            # platform="ios")

# tg_client = TelegramClient(session_file, api_id=random_api_id, api_hash=random_api_hash,app_version=random_app_version,device_model=random_device_model,system_version=random_system_version)


# tg_client = tg_common.easy_sign_in(session_file=session_file)



async def main():


    tg_client = await tg_common.easy_sign_in(session_file=session_file)

    dialogs = await tg_client.cl.get_dialogs()
    print(1)


if __name__ == '__main__':
    asyncio.run(main())