import random
from datetime import datetime, timedelta

from my_modules.my_sqlite3 import MySqlite3


def make_charts_list(
    tg_chats: list[str], tg_chats_db: list[dict[str, str]], db: MySqlite3
) -> dict[str, str]:
    """_summary_.

    :param tg_chats: _description_
    :type tg_chats: list[str]
    :param tg_chats_db: _description_
    :type tg_chats_db: list[dict[str, str]]
    :param db: _description_
    :type db: MySqlite3
    :return: _description_
    :rtype: dict[str, str]
    """
    rez = {}
    for chat in tg_chats:
        for chat_db in tg_chats_db:
            rez.setdefault(chat, []).append(chat_db["send_message"])
            # if (
            #     chat.strip() == chat_db["chat_name"].strip()
            #     and chat_db["last_send_at"]
            #     and chat_db["is_active"]
            # ):
            #     last_send_at = datetime.strptime(  # noqa: DTZ007
            #         chat_db["last_send_at"], "%Y-%m-%d %H:%M:%S"
            #     )
            #     now = datetime.now()
            #     delta = now - last_send_at
            #     if delta.days >= 5:
            #         rez.setdefault(chat, []).append(chat_db["send_message"])
    return rez


def random_waiting(min_time: int = 5, max_time: int = 15) -> int:
    """_summary_.

    :param min_time: _description_, defaults to 1
    :type min_time: int, optional
    :param max_time: _description_, defaults to 5
    :type max_time: int, optional
    :return: _description_
    :rtype: int
    """
    return random.randint(min_time, max_time)  # noqa: S311
