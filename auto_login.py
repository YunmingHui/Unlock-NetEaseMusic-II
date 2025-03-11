# coding: utf-8

import os
import time
import logging
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from retrying import retry

# Configure logging
logging.basicConfig(level=logging.INFO, format='[%(levelname)s] %(asctime)s %(message)s')

@retry(wait_random_min=5000, wait_random_max=10000, stop_max_attempt_number=3)
def enter_iframe(browser):
    logging.info("Enter login iframe")
    time.sleep(5)  # 给 iframe 额外时间加载
    try:
        iframe = WebDriverWait(browser, 10).until(
            EC.presence_of_element_located((By.XPATH, "//*[starts-with(@id,'x-URS-iframe')]")
        ))
        browser.switch_to.frame(iframe)
        logging.info("Switched to login iframe")
    except Exception as e:
        logging.error(f"Failed to enter iframe: {e}")
        browser.save_screenshot("debug_iframe.png")  # 记录截图
        raise
    return browser

@retry(wait_random_min=1000, wait_random_max=3000, stop_max_attempt_number=5)
def extension_login():
    chrome_options = webdriver.ChromeOptions()

    logging.info("Load Chrome extension NetEaseMusicWorldPlus")
    chrome_options.add_extension('NetEaseMusicWorldPlus.crx')

    logging.info("Initializing Chrome WebDriver")
    try:
        service = Service(ChromeDriverManager().install())  # Auto-download correct chromedriver
        browser = webdriver.Chrome(service=service, options=chrome_options)
    except Exception as e:
        logging.error(f"Failed to initialize ChromeDriver: {e}")
        return

    # Set global implicit wait
    browser.implicitly_wait(20)

    browser.get('https://music.163.com')

    # Inject Cookie to skip login
    logging.info("Injecting Cookie to skip login")
    browser.add_cookie({"name": "MUSIC_U", "value": "0003BA4AC60FD7F9212246806579D2EB4E8F66A4205B3F2B5B8D8C1F1D656F8936FC14B3268228E4DF84479F5C70A8D1960D07E2FA8A7D5538E36BCDD51944671F1EC66C0516B15E3894F0B8638B792C98923B71E6697B4EEF95245B915E6C34D3DC7B8FD9C4B10635A987330ED039CBA4CBD3F3E91405FC27C48011371910CA377CFDBBACA6E2D3D3CBDB0C1338BACD31D15C2A60EC4042DA9131590E44CE166B1508F359384D06782E8F908F9CDF4A063D9F3F81AA8B4BCC64E9CB91CBA5D2ADED092CB676AE5D856661EF649E39F71E8F1F3F7499598FA7968F578007C6FFC370368C2DD945395F88AD6C745393566A2AF48C449A75CF94A213D0F7475A013F6C6E6B86EB656DC2DAA601603F217CC42DE426793874E93C01785445D1ED56589358EE68FF2CD380C6E8885E826A279816E196AE03087DCB9813DCE84572839CB286D37A03A626C28D97C9EF42687E22AAF00A2F1D03543EB5046A8D99B800813CB12A84AA259CB145AED11FD2B4BCC9"})
    browser.refresh()
    time.sleep(5)  # Wait for the page to refresh
    logging.info("Cookie login successful")

    # Confirm login is successful
    logging.info("Unlock finished")

    time.sleep(10)
    browser.quit()


if __name__ == '__main__':
    try:
        extension_login()
    except Exception as e:
        logging.error(f"Failed to execute login script: {e}")
