"""Main."""

from pathlib import Path

from patchright.sync_api import Error as PlaywrightError
from patchright.sync_api import TimeoutError as PlaywrightTimeoutError

# Change playwright standart import to patchright
from patchright.sync_api import sync_playwright

from modules import utils
from modules.logger import MyLogger
from modules.pw import MyPW
from modules.sqlite3 import MySqlite3
from modules.tg import MyTg


def main(pw: MyPW, tg: MyTg, db: MySqlite3, logger: MyLogger) -> None:
    """_summary_.

    :param browser: _description_
    :type browser: MyBrowser
    :param db: _description_
    :type db: MySqlite3
    """
    url = "https://web.telegram.org"

    pw.start().start_browser()
    logger.info("Браузер запущен")

    page = pw.get_page(url)
    logger.info(f"Страница {pw.url} загружена")

    tg_chats = tg.set_page(page).get_tg_chats()
    tg_chats_db = db.get_tg_chats()
    chats = utils.make_charts_list(tg_chats, tg_chats_db, db)

    if chats:
        tg.send_message(chats)

    pw.close_browser()
    pw.stop()


if __name__ == "__main__":
    user_data_dir = str(Path("./user_data/chromium").resolve())
    extension_path = str(Path("./extensions/ext").resolve())
    extension_names = utils.get_list_of_extensions(extension_path)

    exclude_chats = ["Telegram", "Saved Messages"]
    db_path = str(Path("./db/database.db").resolve())
    recordings_path = str(Path("./recordings").resolve())

    pw = MyPW(
        user_data_dir=user_data_dir,
        extension_names=extension_names,
        recordings_path=recordings_path,
        is_recording=False,
        is_logging=True,
    )
    db = MySqlite3(db_path)
    logger = MyLogger(logger_name="main", is_logging=True)
    tg = MyTg(
        exclude_chats=exclude_chats,
    )

    try:
        main(pw, tg, db, logger)
    except PlaywrightTimeoutError as e:
        # таймаут при навигации
        logger.exception(f"Таймаут навигации на {pw.url}: {e.message}")
    except PlaywrightError as e:
        # другие ошибки Playwright (сеть, редиректы, etc.)
        logger.exception(f"Ошибка навигации на {pw.url}: {e.message}")
    except Exception as e:
        # другие ошибки
        logger.exception(f"Какая то другая ошибка: {e}")
