# TikTok Video Downloader Bot

Telegram-бот для скачивания видео из TikTok. Отправь ссылку — получи видео.

## Установка

```bash
git clone https://github.com/zfreak1337/tiktok_bot_download.git
cd tiktok_bot_download
pip install -r requirements.txt
```

## Настройка

Открой `bot.py` и замени токен:

```python
BOT_TOKEN = "YOUR_BOT_TOKEN_HERE"
```

Токен можно получить у [@BotFather](https://t.me/BotFather).

## Запуск

```bash
python bot.py
```

Для работы в фоне:

```bash
nohup python bot.py &
```

## Использование

1. Открой бота в Telegram
2. Отправь ссылку на TikTok-видео
3. Бот скачает и отправит видео в чат
