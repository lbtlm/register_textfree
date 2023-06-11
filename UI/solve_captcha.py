import os
import random
from six.moves import urllib

import pydub
from speech_recognition import Recognizer, AudioFile

from utils.LogUtil import logger


class SolveCaptcha:
    def __init__(self, page):
        self.page = page
        self.main_frame = None
        self.recaptcha = None

    async def delay(self):
        await self.page.wait_for_timeout(random.randint(3, 5) * 1000)

    async def presetup(self):

        try:
            name = await self.page.locator(
                "//iframe[@title='reCAPTCHA']").get_attribute("name")
            self.recaptcha = self.page.frame(name=name)

            logger.info("获取到recaptcha的iframe")
            await self.delay()
        except Exception as error:
            logger.info(f"获取recaptcha的iframe失败，{error}")
            return False

        await self.recaptcha.locator("//div[@class='recaptcha-checkbox-border']").click()
        logger.info("点击了recaptcha的checkbox")

        await self.delay()

        while True:

            s = self.recaptcha.locator("//span[@id='recaptcha-anchor']")
            if s is None:
                await self.delay()
                continue
            else:
                logger.info("获取到recaptcha的checkbox")
                break

        anchor_res = await s.get_attribute("aria-checked")
        if anchor_res != "false":
            logger.info("recaptcha的checkbox已经被选中")
            return



        # 点开下层的iframe
        name = await self.page.locator("//iframe[contains(@src,'https://www.google.com/recaptcha/enterprise/bframe?')]").get_attribute("name")
        self.recaptcha_mp3_frame = self.page.frame(name=name)

        logger.info("获取到mp3的iframe")
        await self.delay()

        await self.recaptcha_mp3_frame.locator("id=recaptcha-audio-button").click()
        logger.info("点击了recaptcha的mp3按钮")

        await self.delay()

        return True

    async def start(self):
        setup_res = await self.presetup()
        if setup_res is False:
            return False

        tries = 0
        while tries <= 5:
            await self.delay()
            try:
                solve_res = await self.solve_captcha()
                if solve_res is False:
                    return False

            except Exception as e:
                print(e)
                await self.recaptcha_mp3_frame.locator("id=recaptcha-reload-button").click()
            else:
                s = self.recaptcha.locator("//span[@id='recaptcha-anchor']")
                if await s.get_attribute("aria-checked") != "false":
                    await self.recaptcha_mp3_frame.locator("id=recaptcha-demo-submit").click()
                    await self.delay()
                    return True
            tries += 1

    async def solve_captcha(self):
        while True:  # 等待mp3的iframe加载完成

            s = self.recaptcha_mp3_frame.locator("//button[@aria-labelledby='audio-instructions rc-response-label']")
            if s is None:
                await self.delay()
                continue
            else:
                await s.click()
                logger.info("点击了recaptcha的mp3按钮")
                # break

                if self.recaptcha_mp3_frame.get_by_text("稍后重试"):
                    logger.info("点击了recaptcha的mp3按钮后，出现了稍后重试")

                    return False
                else:
                    break




        # await self.recaptcha_mp3_frame.locator("//button[@aria-labelledby='audio-instructions rc-response-label']").click()
        href = await self.recaptcha_mp3_frame.locator("//a[@class='rc-audiochallenge-tdownload-link']").get_attribute("href")

        urllib.request.urlretrieve(href, "audio.mp3")

        sound = pydub.AudioSegment.from_mp3(
            "audio.mp3").export("audio.wav", format="wav")

        recognizer = Recognizer()

        recaptcha_audio = AudioFile("audio.wav")
        with recaptcha_audio as source:
            audio = recognizer.record(source)

        text = recognizer.recognize_google(audio)
        print(text)
        await self.recaptcha_mp3_frame.locator("id=audio-response").fill(text, timeout=30000)
        await self.delay()
        await self.recaptcha_mp3_frame.locator("id=recaptcha-verify-button").click(timeout=30000)
        await self.delay()

    def __del__(self):
        os.remove("audio.mp3")
        os.remove("audio.wav")
