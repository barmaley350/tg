# ruff: noqa: G004
"""Вспомогательный класс."""

# Change playwright standart import to patchright
from patchright.sync_api import Page

from . import utils
from .logger import MyLogger


class MyTg:
    def __init__(
        self,
        *,
        exclude_chats: list[str],
        is_logging: bool = False,
    ) -> None:
        """_summary_.

        :param user_data_dir: _description_
        :type user_data_dir: str
        :param extension_path: _description_
        :type extension_path: str
        :param extension_names: _description_
        """
        self.page: Page | None = None
        self.exclude_chats = exclude_chats
        self.tg_chats = []
        self.logger = MyLogger(logger_name=__name__, is_logging=is_logging)

    def _exclude_chats(self, chat: str) -> bool:
        """_summary_.

        :param chat: _description_
        :type chat: str
        :return: _description_
        :rtype: bool
        """
        return chat not in self.exclude_chats

    def set_page(self, page: Page) -> "MyTg":
        """_summary_."""
        self.page = page
        return self

    def get_tg_chats(self) -> list[str]:
        """_summary_."""
        if self.page is not None:
            tab = self.page.locator(".menu-horizontal-div-item", has_text="job")
            if tab.is_visible():
                tab.click()
            else:
                self.logger.warning("Нет вкладки job")

            self.page.wait_for_selector(
                "div.chatlist-top ul.chatlist a.chatlist-chat", timeout=10000
            )
            chat_items = self.page.locator(
                "div.chatlist-top ul.chatlist a.chatlist-chat"
            )
            count = chat_items.count()

            for i in range(count):
                # Внутри каждого a ищем span.peer-title
                title = (
                    chat_items
                    .nth(i)
                    .locator("div.dialog-title div.user-title span.peer-title")
                    .inner_text()
                )
                if self._exclude_chats(title):
                    self.tg_chats.append(title)
            return self.tg_chats
        raise ValueError(f"{self.page} is None")

    def send_message(self, d: dict[str, str]) -> None:
        """_summary_.

        :param d: _description_
        :type d: dict[str, str]
        """
        if self.page is not None:
            self.page.wait_for_selector(".chatlist", timeout=180000)
            self.logger.info("Начинаем отправку сообщений")
            self.logger.info(f"Всего групп {len(d)}")
            for idx, (chat_name, chat_message) in enumerate(d.items(), start=1):
                delay = utils.random_waiting()
                self.logger.info(
                    f"#{idx} Задержка {delay} сек. Обрабатываем группу {chat_name}."
                )
                chat_row = self.page.locator(
                    "div.chatlist-top ul.chatlist a.chatlist-chat"
                ).filter(
                    has=self.page.locator(
                        "div.dialog-title div.user-title span.peer-title"
                    ).filter(has_text=chat_name)
                )
                chat_row.click()
                # Нажимаем на кнопку чтобы проматать к последнему сообщению
                # 1. Сколько кнопок с таким классом найдено?
                count = self.page.locator("button.bubbles-go-down").count()
                self.logger.warning(f"Найдено кнопок: {count}")

                button = self.page.locator("button.bubbles-go-down")
                if button.is_visible():
                    button.click()

                self.page.wait_for_timeout(delay * 1000)
