"""Main."""

from pathlib import Path

from patchright.sync_api import Error as PlaywrightError
from patchright.sync_api import TimeoutError as PlaywrightTimeoutError

# Change playwright standart import to patchright
from patchright.sync_api import sync_playwright

from my_modules import utils
from my_modules.my_logger import MyLogger
from my_modules.my_sqlite3 import MySqlite3
from my_modules.my_tg import MyTg


def main(tg: MyTg, db: MySqlite3, logger: MyLogger) -> None:
    """_summary_.

    :param tg: _description_
    :type tg: MyTg
    :param db: _description_
    :type db: MySqlite3
    """
    with sync_playwright() as pw:
        browser = tg.get_browser(pw)
        logger.info(f"Браузер запущен на {tg.tg_url}")

        tg.get_tg_web_page()
        logger.info(f"Страница {tg.tg_url} загружена")

        tg_chats = tg.get_tg_chats()
        tg_chats_db = db.get_tg_chats()
        chats = utils.make_charts_list(tg_chats, tg_chats_db, db)

        if chats:
            tg.send_message(chats)

        browser.close()


if __name__ == "__main__":
    user_data_dir = str(Path("./user_data/chromium").resolve())
    extension_names = [
        # "-VPN-Chrome-Planet-VPN-Chrome",
        # "-VPN-Free-VPN-1VPN-Chrome",
        # "PureVPN-Proxy-VPN-Chrome-Chrome",
        "-VPN-Proxy-YouTube-Browsec-VPN-Chrome",  # job
        # "-VPN-Chrome-VPN-VeePN-Chrome",
    ]
    extension_path = str(Path("./extensions/ext").resolve())
    tg_url = "https://web.telegram.org"
    exclude_chats = ["Telegram", "Saved Messages"]
    db_path = str(Path("./db/database.db").resolve())
    recordings_path = str(Path("./recordings").resolve())

    tg = MyTg(
        user_data_dir=user_data_dir,
        extension_path=extension_path,
        extension_names=extension_names,
        tg_url=tg_url,
        exclude_chats=exclude_chats,
        recordings_path=recordings_path,
        is_recording=False,
        is_logging=True,
    )
    db = MySqlite3(db_path)
    logger = MyLogger(logger_name="main", is_logging=True)

    try:
        main(tg, db, logger)
    except PlaywrightTimeoutError as e:
        # таймаут при навигации
        logger.exception(f"Таймаут навигации на {tg.tg_url}: {e}")
    except PlaywrightError as e:
        # другие ошибки Playwright (сеть, редиректы, etc.)
        logger.exception(f"Ошибка навигации на {tg.tg_url}: {e}")
    except Exception as e:
        # другие ошибки
        logger.exception(f"Какая то другая ошибка: {e}")
