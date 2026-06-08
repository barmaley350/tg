# ruff: noqa: G004
"""Вспомогательный класс."""

# Change playwright standart import to patchright
# Change playwright standart import to patchright
from patchright.sync_api import (
    BrowserContext,
    Page,
    Playwright,
    sync_playwright,
)

from . import utils
from .logger import MyLogger


class MyPW:
    def __init__(
        self,
        *,
        user_data_dir: str,
        extension_names: str,
        # exclude_chats: list[str],
        recordings_path: str,
        is_logging: bool = False,
        is_recording: bool = False,
    ) -> None:
        """_summary_.

        :param user_data_dir: _description_
        :type user_data_dir: str
        :param extension_names: _description_
        :type extension_names: str
        :param exclude_chats: _description_
        :type exclude_chats: list[str]
        :param recordings_path: _description_
        :type recordings_path: str
        :param is_logging: _description_, defaults to False
        :type is_logging: bool, optional
        :param is_recording: _description_, defaults to False
        :type is_recording: bool, optional
        """
        self.browser: BrowserContext | None = None
        self.page: Page | None = None
        self.context: BrowserContext | None = None
        self.user_data_dir = user_data_dir
        self.extension_names = extension_names
        self.is_recording = is_recording
        self.recordings_path = recordings_path
        # self.exclude_chats = exclude_chats
        self.tg_chats = []
        self.logger = MyLogger(logger_name=__name__, is_logging=is_logging)
        self.url = None
        self.playwright: Playwright | None = None

    # def _exclude_chats(self, chat: str) -> bool:
    #     """_summary_.

    #     :param chat: _description_
    #     :type chat: str
    #     :return: _description_
    #     :rtype: bool
    #     """
    #     return chat not in self.exclude_chats

    def set_url(self, url: str | None) -> None:
        """_summary_."""
        if url and url is not None:
            self.url = url

    def start(self) -> "MyPW":
        """_summary_."""
        if self.playwright is None:
            self.playwright = sync_playwright().start()
        return self

    def stop(self) -> None:
        """_summary_."""
        if self.playwright is not None:
            self.playwright.stop()

    def close_browser(self) -> None:
        """_summary_."""
        if self.browser is not None:
            self.browser.close()
            self.logger.info("Закрываем браузер")
            self.browser = None

    def start_browser(self) -> "MyPW":
        """_summary_.

        :param p: _description_
        :type p: Playwright
        """
        params = {
            "user_data_dir": self.user_data_dir,
            # "channel": "chrome",
            "headless": False,
            "args": [
                f"--disable-extensions-except={self.extension_names}",
                f"--load-extension={self.extension_names}",
            ],
        }
        if self.is_recording:
            params["record_video_dir"] = self.recordings_path
            params["record_video_size"] = {"width": 1920, "height": 1080}

        # self.playwright = sync_playwright().start()
        if self.playwright is not None:
            self.browser = self.playwright.chromium.launch_persistent_context(**params)

        return self

    def get_page(self, url: str | None = None) -> Page:
        """_summary_.

        :raises ValueError: _description_
        :return: _description_
        :rtype: Page
        """
        self.set_url(url)

        if self.browser is None:
            raise ValueError("Browser is None")
        if self.url is None:
            raise ValueError("Url is None")

        self.page = self.browser.new_page()
        self.logger.info(f"Открываем страницу {self.url}")
        self.page.goto(
            self.url,
            timeout=120000,
            wait_until="domcontentloaded",
        )

        return self.page

    # def get_tg_chats(self) -> list[str]:
    #     """_summary_."""
    #     if self.page is not None:
    #         tab = self.page.locator(".menu-horizontal-div-item", has_text="job")
    #         if tab.is_visible():
    #             tab.click()
    #         else:
    #             self.logger.warning("Нет вкладки job")

    #         self.page.wait_for_selector(
    #             "div.chatlist-top ul.chatlist a.chatlist-chat", timeout=10000
    #         )
    #         chat_items = self.page.locator(
    #             "div.chatlist-top ul.chatlist a.chatlist-chat"
    #         )
    #         count = chat_items.count()

    #         for i in range(count):
    #             # Внутри каждого a ищем span.peer-title
    #             title = (
    #                 chat_items
    #                 .nth(i)
    #                 .locator("div.dialog-title div.user-title span.peer-title")
    #                 .inner_text()
    #             )
    #             if self._exclude_chats(title):
    #                 self.tg_chats.append(title)
    #         return self.tg_chats
    #     raise ValueError(f"{self.page} is None")

    # def send_message(self, d: dict[str, str]) -> None:
    #     """_summary_.

    #     :param d: _description_
    #     :type d: dict[str, str]
    #     """
    #     if self.page is not None:
    #         self.page.wait_for_selector(".chatlist", timeout=180000)
    #         self.logger.info("Начинаем отправку сообщений")
    #         self.logger.info(f"Всего групп {len(d)}")
    #         for idx, (chat_name, chat_message) in enumerate(d.items(), start=1):
    #             delay = utils.random_waiting()
    #             self.logger.info(
    #                 f"#{idx} Задержка {delay} сек. Обрабатываем группу {chat_name}."
    #             )
    #             chat_row = self.page.locator(
    #                 "div.chatlist-top ul.chatlist a.chatlist-chat"
    #             ).filter(
    #                 has=self.page.locator(
    #                     "div.dialog-title div.user-title span.peer-title"
    #                 ).filter(has_text=chat_name)
    #             )
    #             chat_row.click()
    #             # Нажимаем на кнопку чтобы проматать к последнему сообщению
    #             # 1. Сколько кнопок с таким классом найдено?
    #             count = self.page.locator("button.bubbles-go-down").count()
    #             self.logger.warning(f"Найдено кнопок: {count}")

    #             button = self.page.locator("button.bubbles-go-down")
    #             if button.is_visible():
    #                 button.click()

    #             self.page.wait_for_timeout(delay * 1000)
