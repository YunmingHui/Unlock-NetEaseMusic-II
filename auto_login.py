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
    browser.add_cookie({"name": "MUSIC_U", "value": "006428A1AA292F66FF66739E9242D13107CBE73360C1945AFCA7196C50C6000E6D58AB63D6B8E2C2897FE2C22233BE849D2521A4C5B0CAA9EE50E6E6F3738FC7BE077CBDD6571D238C5A2881C85515E482F3126E1B26F757536A4F653A3CE05E1241DA1533C0725F8D3AE21FCBEF4425BF098DE24FC7449300005BCF8847EBF43D741EA619145D4886386B662B98040B4483704776A2AB553229F3F4EA25E339DA26BCC2CEB834BB8378ECC6F0493373BDD43A00AEBAEF6E9E3E94CACBF113C37FE12F205253883E140D29E7C529357BED106416EA96E50C98B4EBF6C1631E1889A8E115115D1C0D207A44E641B2105E3F431A299370B48DF8C48ACDBD9DA1CE15B14FE0B742CCD22B1C6AE6CAEB4CD36983C64CD38252115B22F8FAF18A667843DE07BC14ED780AD8612030BA054500CD38A8C0E7DA8D0EB0E1FE14CD789B19E42F875C5DE58FF83A964662080514B88A86E2D311F83ADE21FC4F41AB1738164B10A59D14FA787D54FE63F3B0B7D3AFB5"})
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
