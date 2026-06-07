# ruff: noqa: G004
"""Вспомогательный класс для работы с Tg."""

# Change playwright standart import to patchright
from patchright.sync_api import BrowserContext, Page, Playwright

from . import utils
from .my_logger import MyLogger


class MyTg:
    def __init__(
        self,
        *,
        user_data_dir: str,
        extension_path: str,
        extension_names: str,
        tg_url: str,
        exclude_chats: list[str],
        recordings_path: str,
        is_logging: bool = False,
        is_recording: bool = False,
    ) -> None:
        """_summary_.

        :param user_data_dir: _description_
        :type user_data_dir: str
        :param extension_path: _description_
        :type extension_path: str
        :param extension_names: _description_
        :type extension_names: str
        :param tg_url: _description_
        :type tg_url: str
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
        self.extension_path = extension_path
        self.extension_names = extension_names
        self.is_recording = is_recording
        self.recordings_path = recordings_path
        self.tg_url = tg_url
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

    def get_browser(self, p: Playwright) -> BrowserContext:
        """_summary_.

        :param p: _description_
        :type p: Playwright
        """
        params = {
            "user_data_dir": self.user_data_dir,
            "headless": False,
            "args": [
                f"--disable-extensions-except={self.extension_names}",
                f"--load-extension={self.extension_names}",
            ],
        }
        if self.is_recording:
            params["record_video_dir"] = self.recordings_path
            params["record_video_size"] = {"width": 1920, "height": 1080}

        self.browser = p.chromium.launch_persistent_context(**params)
        return self.browser

    def get_tg_web_page(self) -> None:
        """_summary_.

        :raises ValueError: _description_
        """
        if self.browser is not None:
            self.page = self.browser.new_page()
            self.logger.info(f"Открываем страницу {self.tg_url}")
            self.page.goto(
                self.tg_url,
                timeout=120000,
                wait_until="domcontentloaded",
            )
        else:
            raise ValueError(f"{self.browser} is None")

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
                button = self.page.locator("button.bubbles-go-down")
                if button.is_visible():
                    button.click()

                self.page.wait_for_timeout(delay * 1000)
