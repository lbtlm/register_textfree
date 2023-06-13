import asyncio
import os
import random
from typing import Union

from six.moves import urllib

import pydub
from speech_recognition import Recognizer, AudioFile

from setting.GLOBAL import LOG_FILE
from utils.COMMON_UTILS import common_utils
from utils.LogUtil import logger


class SolveCaptcha:
    def __init__(self, page, email):
        self.recaptcha_frame = None
        self.recaptcha_mp3_frame = None
        self.page = page
        self.email = email
        self.main_frame = None
        self.recaptcha = None

    async def delay(self):
        await asyncio.sleep(random.randint(3, 5))

    async def presetup(self) -> Union[bool, str]:
        """
        recaptcha窗口操作

        :return: str 代表无需验证，直接通过；bool 代表需要验证，True代表验证成功，False代表验证失败
        """
        try:
            self.recaptcha_frame = self.page.locator("//iframe[@title='reCAPTCHA']")
            common_utils.insert_log(LOG_FILE, f"账号 {self.email} 获取到recaptcha_frame")
            # await self.delay()
            await asyncio.sleep(1)
        except Exception as error:
            common_utils.insert_log(LOG_FILE, f"账号 {self.email} 获取recaptcha的iframe失败，{error}")
            # common_utils.insert_log(f"账号 {self.email} 获取recaptcha的iframe失败，{error}")
            return False

        try:
            name = await self.recaptcha_frame.get_attribute("name")
            self.recaptcha = self.page.frame(name=name)

            common_utils.insert_log(LOG_FILE, f"账号 {self.email} 获取到recaptcha的iframe")
            # await self.delay()
            await asyncio.sleep(1)
        except Exception as error:
            common_utils.insert_log(LOG_FILE, f"账号 {self.email} 获取recaptcha的iframe失败，{error}")
            return False

        await self.recaptcha.locator("//div[@class='recaptcha-checkbox-border']").click()
        common_utils.insert_log(LOG_FILE, f"账号 {self.email} 点击了recaptcha的checkbox")

        # await self.delay()
        await asyncio.sleep(1)

        while True:

            s = self.recaptcha.locator("//span[@id='recaptcha-anchor']")
            if s is None:
                # await self.delay()
                # await asyncio.sleep(1)
                continue
            else:
                common_utils.insert_log(LOG_FILE, f"账号 {self.email} 获取到recaptcha的界面")
                # await self.delay()
                # await asyncio.sleep(1)
                break

        anchor_res = await s.get_attribute("aria-checked")
        if anchor_res != "false":
            common_utils.insert_log(LOG_FILE, f"账号 {self.email} recaptcha的checkbox已经被选中")
            return "success"

        # 点开下层的iframe
        name = await self.page.locator("//iframe[contains(@src,'https://www.google.com/recaptcha/enterprise/bframe?')]").get_attribute("name")
        common_utils.insert_log(LOG_FILE, f"账号 {self.email} name:{name}")
        self.recaptcha_mp3_frame = self.page.frame(name=name)
        common_utils.insert_log(LOG_FILE, f"账号 {self.email} recaptcha_mp3_frame:{self.recaptcha_mp3_frame}")
        common_utils.insert_log(LOG_FILE, f"账号 {self.email} 获取到mp3的iframe")
        # await self.delay()
        # await asyncio.sleep(1)
        return True

    async def start(self) -> bool:
        """
        开始人机验证

        :return:  True 人机验证通过  False 人机验证失败
        """
        setup_res = await self.presetup()
        if isinstance(setup_res, str):
            common_utils.insert_log(LOG_FILE, f"账号 {self.email} 人机验证已经通过")
            return True
        else:
            if setup_res is False:
                return False

        tries = 0
        while tries <= 5:
            await asyncio.sleep(1)
            try:

                solve_res = await self.solve_captcha()
                if solve_res is False:
                    return False
                else:
                    common_utils.insert_log(LOG_FILE, f"账号 {self.email} 人机验证通过")
                    return True

            except Exception as e:
                common_utils.insert_log(LOG_FILE, f"账号 {self.email} error:{e}")
                await self.recaptcha_mp3_frame.locator("id=recaptcha-reload-button").click()

            tries += 1

    async def solve_captcha(self):

        mp3_click_locator, down_load_url_locator = None, None

        common_utils.insert_log(LOG_FILE, f"账号 {self.email} 开始点击MP3按钮")
        one_click = 0
        while True:
            if one_click > 0:
                await self.recaptcha.locator("//div[@class='recaptcha-checkbox-border']").click()
                common_utils.insert_log(LOG_FILE, f"账号 {self.email} 点击了recaptcha的checkbox")
                await self.delay()

            one_click += 1
            # mp = self.recaptcha_mp3_frame.locator("button[id='recaptcha-audio-button']")
            mp = self.recaptcha_mp3_frame.get_by_role("button", name="Get an audio challenge")
            common_utils.insert_log(LOG_FILE, f"账号 {self.email} mp：{mp}")
            if mp is None:
                await self.delay()
                continue
            else:
                await mp.click(timeout=30000)
                common_utils.insert_log(LOG_FILE, f"账号 {self.email} 点击了MP3按钮")
                await self.delay()

                mp3_click_locator = await self.recaptcha_mp3_frame.query_selector("//div[@class='rc-doscaptcha-header-text']")
                common_utils.insert_log(LOG_FILE, f"账号 {self.email} mp3_click_locator：{mp3_click_locator}")



                down_load_url_locator = await self.recaptcha_mp3_frame.query_selector("//a[@class='rc-audiochallenge-tdownload-link']")
                common_utils.insert_log(LOG_FILE, f"账号 {self.email} down_load_url_locator：{down_load_url_locator}")

                if mp3_click_locator is not None or down_load_url_locator is not None:
                    break

            # common_utils.insert_log(LOG_FILE, f"账号 {self.email} mp：{mp}")
            # await mp.click(timeout=30000)

            # common_utils.insert_log(LOG_FILE, f"账号 {self.email} 点击了recaptcha的mp3按钮")
            # await self.delay()
            # await asyncio.sleep(10000)

            # mp3_click_locator = await self.recaptcha_mp3_frame.query_selector("//div[@class='rc-doscaptcha-header-text']")
            # common_utils.insert_log(LOG_FILE, f"账号 {self.email} mp3_click_locator：{mp3_click_locator}")
            # down_load_url_locator = await self.recaptcha_mp3_frame.query_selector("//a[@class='rc-audiochallenge-tdownload-link']")
            # common_utils.insert_log(LOG_FILE, f"账号 {self.email} down_load_url_locator：{down_load_url_locator}")

            if mp3_click_locator is not None:
                mp3_click_locator_text = await mp3_click_locator.inner_text()
                print(mp3_click_locator_text)
                if "稍后重试" in mp3_click_locator_text or "Try again later" in mp3_click_locator_text:
                    common_utils.insert_log(LOG_FILE, f"账号 {self.email} IP被封禁，强制关闭浏览器！")

                    await self.page.close()
                    return False
            elif down_load_url_locator is not None:
                common_utils.insert_log(LOG_FILE, f"账号 {self.email} 检测到MP3下载链接，开始下载！")
                break
            else:
                common_utils.insert_log(LOG_FILE, f"账号 {self.email} 未点击到MP3按钮，重新点击！")
                await asyncio.sleep(1)

        while True:
            href = await down_load_url_locator.get_attribute("href")
            common_utils.insert_log(LOG_FILE, f"账号 {self.email} 获取到MP3下载链接：{href}")

            urllib.request.urlretrieve(href, f"{self.email}.mp3")

            sound = pydub.AudioSegment.from_mp3(f"{self.email}.mp3").export(f"{self.email}.wav", format="wav")

            recognizer = Recognizer()

            recaptcha_audio = AudioFile(f"{self.email}.wav")
            with recaptcha_audio as source:
                audio = recognizer.record(source)

            text = recognizer.recognize_google(audio)
            common_utils.insert_log(LOG_FILE, f"账号 {self.email} 识别到MP3中的文字：{text}")
            await self.recaptcha_mp3_frame.locator("id=audio-response").fill(text, timeout=300000)
            # await self.delay()

            await asyncio.sleep(6)
            await self.recaptcha_mp3_frame.locator("//button[@id='recaptcha-verify-button']").click(timeout=300000)
            await self.delay()
            try:
                s = self.recaptcha.locator("//span[@id='recaptcha-anchor']")
                anchor_res = await s.get_attribute("aria-checked")
                if anchor_res != "false":
                    common_utils.insert_log(LOG_FILE, f"账号 {self.email} recaptcha的checkbox已经被选中")
                    break
            except Exception as e:
                common_utils.insert_log(LOG_FILE, f"账号 {self.email} 判断是否已经验证成功时出错：{e}")
                await self.delay()
            await self.recaptcha.locator("//div[@class='recaptcha-checkbox-border']").click()
            common_utils.insert_log(LOG_FILE, f"账号 {self.email} 点击了recaptcha的checkbox")

        return True

    def __del__(self):
        if os.path.exists(f"{self.email}.mp3"):
            os.remove(f"{self.email}.mp3")
        if os.path.exists(f"{self.email}.wav"):
            os.remove(f"{self.email}.wav")
