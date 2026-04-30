from selenium.webdriver.remote.webdriver import WebDriver
import pyttsx3
from core.config import Config
from services.chess.automation import open_chess_session
from core.windows_utility import apply_dual_chrome_layout

def init_system():
    speaker_engine = pyttsx3.init()

    online_driver = open_chess_session(
        Config.ONLINE_PORT,
        Config.ONLINE_PROFILE_DIR,
        Config.ONLINE_CHESS_LINK
    )
    print("[-] Online ready")

    bot_driver = open_chess_session(
        Config.BOT_PORT,
        Config.BOT_PROFILE_DIR,
        Config.BOT_CHESS_LINK
    )
    print("[-] Bot ready")

    apply_dual_chrome_layout(online_driver, bot_driver)
    print("[-] Dual Chrome layout applied")

    return speaker_engine, online_driver, bot_driver

def stop_system(speaker_engine, online_driver: WebDriver, bot_driver: WebDriver):
    speaker_engine.stop()

    try:
        online_driver.quit()
    except:
        pass

    try:
        bot_driver.quit()
    except:
        pass