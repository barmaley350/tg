# Парсер tg каналов

```
uv sync
```
Используется `patchright` вместо `playwright`
Тесты на `https://www.todetect.net/bot-detection/` проходит на 100%

При неоходимости установите зависимости 
```
playwright install-deps
```
При неоходимости установите браузеры. Работает только chromium
```
playwright install chromium
```
Поддерживает расширения. Если у вас проблемы с доступом в tg сказайте расширение и положите в папку `./extensions/ext/`

```
drwxrwxr-x  9 home home 4.0K Jun  8 01:13 ./extensions/ext/-VPN-Proxy-YouTube-Browsec-VPN-Chrome/
```