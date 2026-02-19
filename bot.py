<<<<<<< HEAD
import os
import logging
from telegram import Update, InlineKeyboardMarkup, InlineKeyboardButton, WebAppInfo
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO,
)

# ─── НАСТРОЙКИ ────────────────────────────────────────────────────────────────
# Токен берётся из переменной окружения BOT_TOKEN (безопасно для сервера).
# Для локального запуска: задайте переменную в системе или замените None на строку.
BOT_TOKEN  = os.getenv("BOT_TOKEN",  "8307968280:AAGMDecHv0nJcrQ4hySBkYbqnjh7u2OiHqU")
WEBAPP_URL = os.getenv("WEBAPP_URL", "https://oneclickrar-tech.github.io/road-app/")
PROXY      = os.getenv("PROXY", None)   # необязательно, только если нужен прокси
# ──────────────────────────────────────────────────────────────────────────────


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    keyboard = InlineKeyboardMarkup([
        [InlineKeyboardButton(
            text="📋 Программа работ 2026",
            web_app=WebAppInfo(url=WEBAPP_URL),
        )]
    ])
    await update.message.reply_text(
        "Нажмите кнопку ниже для просмотра программы работ по ремонту дорог:",
        reply_markup=keyboard,
    )


async def help_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text(
        "Доступные команды:\n"
        "/start — открыть программу работ\n"
        "/help  — справка"
    )


if __name__ == "__main__":
    builder = ApplicationBuilder().token(BOT_TOKEN)
    if PROXY:
        builder = builder.proxy(PROXY).get_updates_proxy(PROXY)
    app = builder.build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("help", help_cmd))
    print("Бот запущен. Нажмите Ctrl+C для остановки.")
    app.run_polling()
=======
import os
import logging
from telegram import Update, InlineKeyboardMarkup, InlineKeyboardButton, WebAppInfo
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO,
)

# ─── НАСТРОЙКИ ────────────────────────────────────────────────────────────────
# Токен берётся из переменной окружения BOT_TOKEN (безопасно для сервера).
# Для локального запуска: задайте переменную в системе или замените None на строку.
BOT_TOKEN  = os.getenv("BOT_TOKEN",  "8307968280:AAGMDecHv0nJcrQ4hySBkYbqnjh7u2OiHqU")
WEBAPP_URL = os.getenv("WEBAPP_URL", "https://oneclickrar-tech.github.io/road-app/")
PROXY      = os.getenv("PROXY")   # необязательно, только если нужен прокси
# ──────────────────────────────────────────────────────────────────────────────


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    keyboard = InlineKeyboardMarkup([
        [InlineKeyboardButton(
            text="📋 Программа работ 2026",
            web_app=WebAppInfo(url=WEBAPP_URL),
        )]
    ])
    await update.message.reply_text(
        "Нажмите кнопку ниже для просмотра программы работ по ремонту дорог:",
        reply_markup=keyboard,
    )


async def help_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text(
        "Доступные команды:\n"
        "/start — открыть программу работ\n"
        "/help  — справка"
    )


if __name__ == "__main__":
    builder = ApplicationBuilder().token(BOT_TOKEN)
    if PROXY:
        builder = builder.proxy(PROXY).get_updates_proxy(PROXY)
    app = builder.build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("help", help_cmd))
    print("Бот запущен. Нажмите Ctrl+C для остановки.")
    app.run_polling()
>>>>>>> 15bf040375bb8732d64c8339bb43f87038c145d6
