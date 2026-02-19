import os
import logging
from telegram import Update, InlineKeyboardMarkup, InlineKeyboardButton, WebAppInfo
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO,
)

# ─── НАСТРОЙКИ ────────────────────────────────────────────────────────────────
BOT_TOKEN      = os.getenv("BOT_TOKEN",  "8307968280:AAGMDecHv0nJcrQ4hySBkYbqnjh7u2OiHqU")
WEBAPP_URL     = os.getenv("WEBAPP_URL", "https://oneclickrar-tech.github.io/road-app/")
PROXY          = os.getenv("PROXY", None)

# Ваш Telegram username без @ (тот же, что в index.html и admin.html)
ADMIN_USERNAME = os.getenv("ADMIN_USERNAME", "Eveningwint")  # без @
# ──────────────────────────────────────────────────────────────────────────────

ADMIN_URL = WEBAPP_URL.rstrip("/") + "/webapp/admin.html"


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


async def admin_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user = update.effective_user
    if not user or (user.username or "").lower() != ADMIN_USERNAME.lower():
        await update.message.reply_text("⛔ Эта команда только для администратора.")
        return

    keyboard = InlineKeyboardMarkup([
        [InlineKeyboardButton(
            text="⚙️ Управление доступом",
            web_app=WebAppInfo(url=ADMIN_URL),
        )]
    ])
    await update.message.reply_text(
        "Панель администратора:",
        reply_markup=keyboard,
    )


async def help_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text(
        "Доступные команды:\n"
        "/start — открыть программу работ\n"
        "/admin — панель администратора\n"
        "/help  — справка"
    )


if __name__ == "__main__":
    builder = ApplicationBuilder().token(BOT_TOKEN)
    if PROXY:
        builder = builder.proxy(PROXY).get_updates_proxy(PROXY)
    app = builder.build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("admin", admin_cmd))
    app.add_handler(CommandHandler("help", help_cmd))
    print("Бот запущен. Нажмите Ctrl+C для остановки.")
    app.run_polling()
