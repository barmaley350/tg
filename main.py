import time
from pathlib import Path

# Change playwright standart import to patchright
from patchright.sync_api import sync_playwright

TG_WEB = "https://web.telegram.org"
CHAT_NAME = "Python Job | Вакансии | Стажировки"
MESSAGE_TEXT = "Это тестовое сообщение, отправленное через Playwright"

user_data_dir = Path("./user_data/chromium").resolve()
extension_name = "-VPN-Proxy-YouTube-Browsec-VPN-Chrome"
extension_path = Path(f"./extensions/ext/{extension_name}").resolve()


def send_telegram_message():
    with sync_playwright() as p:
        # Важно: headless=False, чтобы видеть, что происходит, и при необходимости вручную подтвердить вход
        browser = p.chromium.launch_persistent_context(
            user_data_dir,
            headless=False,
            args=[
                f"--disable-extensions-except={extension_path}",
                f"--load-extension={extension_path}",
            ],
        )
        page = browser.new_page()
        page.goto(
            TG_WEB,
            timeout=120000,
            wait_until="domcontentloaded",
        )

        # На этом этапе пользователь должен вручную войти в аккаунт (QR/код)
        # Скрипт ждёт, пока появится список чатов (простой эвристический индикатор входа)
        page.wait_for_selector(".chatlist", timeout=180000)

        # Ищем чат по тексту (это хрупкий селектор — может сломаться при обновлении Telegram)
        chat_row = page.locator("a.row.row-clickable.chatlist-chat").filter(
            has=page.locator(".peer-title").filter(has_text=CHAT_NAME)
        )
        # chat_row.first.wait_for(state="visible", timeout=180000)
        chat_row.first.click()

        last_group = page.locator(".bubbles-group.bubbles-group-last")
        # last_group.first.wait_for(
        #     state="visible", timeout=30000
        # )  # ждём, пока подгрузится
        last_group.first.scroll_into_view_if_needed()
        page.wait_for_timeout(500)  # даём время на завершение анимации скролла

        replies_button = last_group.first.locator(".replies.replies-footer")
        # Ждём, пока он станет кликабельным, и кликаем
        replies_button.click()
        # # Ждём появления поля ввода
        # input_area = page.locator('textarea[data-testid="MessageInput"]')
        # input_area.wait_for(state="visible", timeout=30000)

        # input_area.click()
        # input_area.fill(MESSAGE_TEXT)
        # input_area.press("Enter")

        time.sleep(30)  # небольшая пауза, чтобы Telegram успел отправить

        browser.close()


if __name__ == "__main__":
    send_telegram_message()
