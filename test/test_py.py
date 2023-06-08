import re
import time

from playwright.sync_api import Playwright, sync_playwright, expect


def run(playwright: Playwright) -> None:
    browser = playwright.firefox.launch(headless=False)
    context = browser.new_context(
        proxy={"server": "http://16.kookeey.info:37400",
               "username": "97d60162",
               "password": "0d258493"
               }
    )
    page = context.new_page()
    page.goto("https://web.telegram.org/k/")

    # context2 = browser.new_context(
    #     proxy={"server": "http://16.kookeey.info:37400",
    #            "username": "97d60162",
    #            "password": "0d258493"
    #            }
    # )
    # page2 = context2.new_page()
    # page2.goto("https://www.baidu.com")

    # context3 = browser.new_context(
    #     proxy={"server": "http://16.kookeey.info:37400",
    #            "username": "97d60162",
    #            "password": "0d258493"
    #            }
    # )
    # page3 = context3.new_page()
    # page3.goto("https://www.google.com")

    page2 = context.new_page()
    page2.goto("https://www.baidu.com")

    page3 = context.new_page()
    page3.goto("https://www.google.com")

    page.pause()
    page2.pause()
    page3.pause()

    page.get_by_role("button", name="Log in by phone Number").click()
    # time.sleep(10)
    input_phone_field = page.locator("div").filter(has_text=re.compile(r"^\+\d+$"))

    input_phone_field.click()

    for _ in range(10):
        page.keyboard.press('Backspace')
        page.wait_for_timeout(100)

    page.wait_for_timeout(500)

    phone_number = "13074077897"

    page.locator("css=div.input-field.input-field-phone > div.input-field-input").first.type(phone_number)
    page.locator("label").filter(has_text="Keep me signed in").locator("div").first.click()

    page.get_by_role("button", name="Next").click()
    code = input("请输入验证码：")
    page.get_by_role("textbox").fill(code)
    twofa_code = input("请输入2fa验证码：")
    page.locator("input[name=\"notsearch_password\"]").fill(twofa_code)
    page.get_by_role("button", name="Next").click()
    page.get_by_placeholder("Search").click()
    page.get_by_placeholder("Search").fill("@premiumbot")
    page.get_by_text("@PremiumBotPremium Bot").click()
    page.get_by_role("button", name="START").click()
    page.get_by_role("button", name=" Pay CN¥25.00").click()
    page.locator("div").filter(has_text=re.compile(r"^Payment methodPayment method$")).locator("div").first.click()
    page.locator("input[type=\"text\"]").nth(1).click()

    # ---------------------
    context.close()
    browser.close()


with sync_playwright() as playwright:
    run(playwright)
