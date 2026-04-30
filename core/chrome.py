from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import WebDriverException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import requests
import time
import subprocess
from core.config import Config

def switch_to_tab_by_url(driver: WebDriver, url_fragment: str) -> bool:
    for h in driver.window_handles:
        driver.switch_to.window(h)

        if url_fragment in driver.current_url:
            return True

    return False

def launch_chrome(debug_port, user_data_dir, url):
    subprocess.Popen([
        Config.CHROME_PATH,
        f"--app={url}",
        f"--remote-debugging-port={debug_port}",
        f"--user-data-dir={user_data_dir}"
    ])

    url = f"http://{Config.LOCALHOST}:{debug_port}/json"

    # wait for chrome
    start = time.time()
    while time.time() - start < Config.CHROME_LAUNCH_TIMEOUT: 
        try:
            r = requests.get(url)
            if r.status_code == 200: # success code
                return True
        except:
            pass

        return False

def open_chrome_driver_when_ready(address, timeout=Config.CHROME_LAUNCH_TIMEOUT):
    chrome_options = Options()
    chrome_options.debugger_address = address

    for _ in range(timeout * Config.CHROME_LAUNCH_TIMEOUT): 
        try:
            driver = webdriver.Chrome(options=chrome_options)

            _ = driver.current_window_handle
            return driver

        except WebDriverException:
            continue

    raise TimeoutError("Chrome debugger not ready")