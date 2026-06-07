from pathlib import Path

# Change playwright standart import to patchright
from patchright.sync_api import Error, sync_playwright
from patchright.sync_api import TimeoutError as PlaywrightTimeoutError

from my_modules import utils
from my_modules.my_sqlite3 import MySqlite3
from my_modules.my_tg import MyTg


def main(tg: MyTg, db: MySqlite3) -> None:
    """_summary_.

    :param tg: _description_
    :type tg: MyTg
    :param db: _description_
    :type db: MySqlite3
    """
    with sync_playwright() as pw:
        tg.make_browser(pw)
        tg.get_tg_web_page()
        tg_chats = tg.get_tg_chats()
        tg_chats_db = db.get_tg_chats()
        chats = utils.make_charts_list(tg_chats, tg_chats_db, db)

        if chats:
            tg.send_message(chats)


if __name__ == "__main__":
    user_data_dir = str(Path("./user_data/chromium").resolve())
    extension_names = [
        "-VPN-Proxy-YouTube-Browsec-VPN-Chrome",
        # "-VPN-Chrome-VPN-VeePN-Chrome",
    ]
    extension_path = str(Path("./extensions/ext").resolve())
    tg_url = "https://web.telegram.org"
    exclude_chats = ["Telegram", "Saved Messages"]
    db_path = str(Path("./db/database.db").resolve())

    tg = MyTg(user_data_dir, extension_path, extension_names, tg_url, exclude_chats)
    db = MySqlite3(db_path)

    try:
        main(tg, db)
    except PlaywrightTimeoutError as e:
        # таймаут при навигации
        print(f"Таймаут навигации на {tg.tg_url}")
    except Error as e:
        # другие ошибки Playwright (сеть, редиректы, etc.)
        print(f"Ошибка навигации на {tg.tg_url}: {e}")
    except Exception as e:
        # другие ошибки
        print(f"Какая то другая ошибка: {e}")
