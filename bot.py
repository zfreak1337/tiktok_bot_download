import os
import re
import tempfile
import logging

import yt_dlp
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters

BOT_TOKEN = "YOUR_BOT_TOKEN_HERE"

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO,
)
logger = logging.getLogger(__name__)

TIKTOK_REGEX = re.compile(
    r"https?://(?:www\.|vm\.|vt\.)?tiktok\.com/\S+"
)
MAX_FILE_SIZE = 50 * 1024 * 1024  # 50 MB — лимит Telegram


async def start(update: Update, context) -> None:
    await update.message.reply_text(
        "Привет! Отправь мне ссылку на TikTok-видео."
    )


async def handle_message(update: Update, context) -> None:
    text = update.message.text or ""
    match = TIKTOK_REGEX.search(text)

    if not match:
        await update.message.reply_text(
            "Отправь ссылку на TikTok-видео (например, https://vm.tiktok.com/...)."
        )
        return

    url = match.group(0)
    status_msg = await update.message.reply_text("Скачиваю видео...")

    tmp_dir = tempfile.mkdtemp()
    output_path = os.path.join(tmp_dir, "video.mp4")

    ydl_opts = {
        "outtmpl": output_path,
        "format": "best[ext=mp4]/best",
        "quiet": True,
        "no_warnings": True,
        "noplaylist": True,
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])

        if not os.path.exists(output_path):
            await status_msg.edit_text("Не удалось скачать видео. Проверь ссылку.")
            return

        file_size = os.path.getsize(output_path)
        if file_size > MAX_FILE_SIZE:
            await status_msg.edit_text(
                "Видео слишком большое (>50 МБ) для отправки через Telegram."
            )
            return

        await status_msg.edit_text("Отправляю видео...")

        with open(output_path, "rb") as video_file:
            await update.message.reply_video(
                video=video_file,
                supports_streaming=True,
            )

        await status_msg.delete()

    except yt_dlp.utils.DownloadError:
        await status_msg.edit_text(
            "Ошибка скачивания. Проверь ссылку — возможно, видео удалено или приватное."
        )
    except Exception as e:
        logger.error("Unexpected error: %s", e)
        await status_msg.edit_text("Произошла ошибка. Попробуй ещё раз позже.")
    finally:
        if os.path.exists(output_path):
            os.remove(output_path)
        if os.path.exists(tmp_dir):
            os.rmdir(tmp_dir)


def main() -> None:
    app = Application.builder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    logger.info("Бот запущен")
    app.run_polling()


if __name__ == "__main__":
    main()
