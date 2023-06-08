import asyncio
import logging
import random
import re
import threading
import time
from pathlib import Path

from playwright.async_api import async_playwright, Playwright

from utils.COMMON_UTILS import common_utils

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

dir_path = r"C:\Users\55049\PycharmProjects\subscribe_premium\session"

session_files = common_utils.get_session_list(Path(dir_path))

print(session_files)


async def do_subscribe_premium(playwright: Playwright, phone_number: str):
    # return

    try:

        # browser = await playwright.firefox.launch(headless=False)  # ,  # 70.kookeey.info:11988 )
        browser = await playwright.chromium.launch(headless=False)  # ,  # 70.kookeey.info:11988 )

        page = await  browser.new_page()

        await page.goto("https://web.telegram.org/k/")
        logging.info(f"账号 {phone_number} 正在登录...")

        await page.get_by_role("button", name="Log in by phone Number").click()  # +15878843622.session
        # time.sleep(10)
        input_phone_field = page.locator("div").filter(has_text=re.compile(r"^\+\d+$"))

        await input_phone_field.click()

        for _ in range(10):
            await page.keyboard.press('Backspace')
            await page.wait_for_timeout(100)

        await page.locator("css=div.input-field.input-field-phone > div.input-field-input").first.type(text=phone_number, timeout=5000)
        await page.locator("label").filter(has_text="Keep me signed in").locator("div").first.click()

        # return

        await page.get_by_role("button", name="Next").click()

        while True:
            if self.code_dict[phone_number] == 0:
                logging.info(f"账号 {phone_number} 等待验证码！")
                await page.wait_for_timeout(5000)
            else:
                logging.info(f"账号 {phone_number} 获取到验证码 {self.code_dict[phone_number]} ！")
                await page.wait_for_timeout(3000)
                await page.get_by_role("textbox").fill(self.code_dict[phone_number])
                break

        # 输入验证码完成 ，检测是否需要二级密码
        await page.locator("input[name=\"notsearch_password\"]").fill(self.two_fa_var.get())
        logging.info(f"账号 {phone_number} 输入二级密码完成！")
        await page.wait_for_timeout(3000)
        await page.get_by_role("button", name="Next").click()
        await page.wait_for_timeout(3000)

        await page.get_by_placeholder("Search").click()
        await page.wait_for_timeout(3000)
        await page.get_by_placeholder("Search").fill("@premiumbot")
        await page.wait_for_timeout(3000)
        await page.get_by_text("@PremiumBotPremium Bot").click()
        await page.wait_for_timeout(3000)
        await page.get_by_role("button", name="START").click()
        await page.wait_for_timeout(3000)

        logging.info(f"账号 {phone_number} 开始订阅！")

        await page.locator("button").filter(has_text=re.compile(r"^Pay.*$")).click()
        await page.wait_for_timeout(3000)

        await page.locator("div").filter(has_text=re.compile(r"^Payment methodPayment method$")).locator("div").first.click()
        await page.wait_for_timeout(3000)
        await page.locator("input[type=\"text\"]").nth(1).click()
        await page.wait_for_timeout(3000)
        await page.locator("input[type=\"text\"]").nth(1).type(card_number)
        logging.info(f"账号 {phone_number} 输入信用卡号 {card_number} 完成！")
        await page.wait_for_timeout(1000)
        await page.locator("input[type=\"text\"]").nth(2).click()
        await page.wait_for_timeout(1000)
        await page.locator("input[type=\"text\"]").nth(2).type(card_date)
        logging.info(f"账号 {phone_number} 输入信用卡号 {card_date} 完成！")
        await page.wait_for_timeout(1000)
        await page.locator("input[name=\"notsearch_password\"]").click()
        await page.wait_for_timeout(3000)
        await page.locator("input[name=\"notsearch_password\"]").type(card_cvv)
        logging.info(f"账号 {phone_number} 输入信用卡校检码 {card_cvv} 完成！")

        await page.wait_for_timeout(1000)
        await page.get_by_role("button", name="PROCEED TO CHECKOUT").click()
        await page.wait_for_timeout(5000)
        logging.info(f"账号 {phone_number} 开始支付！")

        pay_button = page.locator("css=button.payment-item-pay").first
        while await pay_button.is_disabled(timeout=1000):
            await page.locator(".scrollable > label > .c-ripple").click(
                force=True,
                position=Position({
                    "x": 20,
                    "y": 25
                })
            )

            await page.wait_for_timeout(1000)

        logging.info("选中 同意支付条款！")
        logging.info(f"账号 {phone_number} 开始检测卡号是否有效！")

        await page.wait_for_timeout(3000)

        await page.locator("button").filter(has_text=re.compile(r"^PAY.*$")).click()
        # await page.wait_for_timeout(10000)
        # await page.goto("https://web.telegram.org/k/#@PremiumBot")

        await page.get_by_role("img", name="🎁").click(timeout=60000)

        logging.info(f"账号 {phone_number} 开通会员成功！")

        # 转移成功的 session 到 success 文件夹

        common_utils.credit_card_times_subtraction(file_path=Path(self.card_path_var.get()), card_number=card_number)

        return True
    except Exception as e:
        logging.info(f"账号 {phone_number} 开通会员失败，原因：{e}")
        return False


async def subscribe_premium(session_file):
    phone_number = Path(session_file).stem
    logging.info(f"账号 {phone_number} 正在进行浏览器登录...")
    # return
    async with async_playwright() as playwright:
        subscribe_premium_res = await do_subscribe_premium(playwright=playwright, phone_number=phone_number)

    logging.info(f"send {Path(session_file).stem} start")
    sleep_time = random.randint(1, 9)
    await asyncio.sleep(sleep_time)
    logging.info(f"send {Path(session_file).stem} end ,耗时 {sleep_time} 秒 ")


def start_new(session_file, sem):
    with sem:
        # loop = asyncio.new_event_loop()
        # loop.run_until_complete(subscribe_premium(session_file=session_file))

        # self.subscribe_premium(session_file=session_file)
        try:
            loop = asyncio.new_event_loop()
            loop.run_until_complete(subscribe_premium(session_file=session_file))
        except asyncio.CancelledError as cancel_error:
            logging.info(f"loop被强制取消，触发取消错误：{cancel_error}")

        except Exception as error:
            logging.info(f"触发其他错误：{error}")
        finally:
            logging.info(f"loop关闭")
            loop.close()


def main():
    session_files = common_utils.get_session_list(Path(dir_path))
    # 获取线程数
    thread_num = 5
    # sem = asyncio.Semaphore(thread_num)
    sem = threading.Semaphore(thread_num)

    # 空session文件夹
    if not session_files:
        logging.info('没有找到session文件，请检查sessions文件夹！')
    else:
        # 正常文件夹
        tasks_num = len(session_files)

        threads = []
        for num in range(tasks_num):
            t = threading.Thread(target=start_new, args=(session_files[num], sem))
            threads.append(t)
            t.daemon = True
            t.start()

        for item in threads:
            item.join()
            time.sleep(0.1)

            # t.join()
        # time.sleep(10)


if __name__ == '__main__':
    main()
