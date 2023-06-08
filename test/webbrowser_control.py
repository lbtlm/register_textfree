import time
from pathlib import Path

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from setting.GLOBAL import CHROME_PATH
from utils.COMMON_UTILS import common_utils


class WebBrowserControl:
    def __init__(self, proxy_str):
        self.service = Service(executable_path=CHROME_PATH)

        chromeOptions = webdriver.ChromeOptions()
        # 设置代理
        chromeOptions.add_argument(f"--proxy-server={proxy_str}")
        self.driver = webdriver.Chrome(service=self.service, options=chromeOptions)
        self.wait = WebDriverWait(self.driver, 20)


    def get(self, url):
        self.driver.get(url)

    def find_element(self, by, value):
        return self.wait.until(EC.presence_of_element_located((by, value)))

    def find_elements(self, by, value):
        return self.wait.until(EC.presence_of_all_elements_located((by, value)))

    def click(self, element):
        element.click()

    def send_keys(self, element, keys):
        element.send_keys(keys)

    def close(self):
        self.driver.close()

# proxy_str = common_utils.get_random_line(Path(r"C:\Users\55049\PycharmProjects\subscribe_premium\test\proxy_txt.txt"))
proxy_str = "http://70.kookeey.info:11988"
web_control = WebBrowserControl(proxy_str)
# web_control.get("https://web.telegram.org/k/")
web_control.get("https://www.google.com")

time.sleep(20)

print(web_control.driver.title)

web_control.close()
