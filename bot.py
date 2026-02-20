import os
import json
import logging
import urllib.request
import tempfile
from io import BytesIO

from telegram import Update, InlineKeyboardMarkup, InlineKeyboardButton, WebAppInfo
from telegram.ext import (
    ApplicationBuilder, CommandHandler, MessageHandler,
    ContextTypes, filters,
)
from fpdf import FPDF

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO,
)

# ─── НАСТРОЙКИ ────────────────────────────────────────────────────────────────
BOT_TOKEN      = os.getenv("BOT_TOKEN",  "8307968280:AAGMDecHv0nJcrQ4hySBkYbqnjh7u2OiHqU")
WEBAPP_URL     = os.getenv("WEBAPP_URL", "https://oneclickrar-tech.github.io/road-app/")
PROXY          = os.getenv("PROXY", None)
ADMIN_USERNAME = os.getenv("ADMIN_USERNAME", "Eveningwint")  # без @
# ──────────────────────────────────────────────────────────────────────────────

ADMIN_URL = WEBAPP_URL.rstrip("/") + "/webapp/admin.html"

# Шрифты кэшируются в /tmp при первом запросе
_FONT_DIR = tempfile.gettempdir()
_FONT_REG  = os.path.join(_FONT_DIR, "DejaVuSans.ttf")
_FONT_BOLD = os.path.join(_FONT_DIR, "DejaVuSans-Bold.ttf")

_FONT_URLS = {
    _FONT_REG:  "https://raw.githubusercontent.com/dejavu-fonts/dejavu-fonts/master/ttf/DejaVuSans.ttf",
    _FONT_BOLD: "https://raw.githubusercontent.com/dejavu-fonts/dejavu-fonts/master/ttf/DejaVuSans-Bold.ttf",
}


def ensure_fonts() -> None:
    for path, url in _FONT_URLS.items():
        if not os.path.exists(path):
            logging.info("Загружаем шрифт: %s", url)
            urllib.request.urlretrieve(url, path)


def generate_pdf(obj_name: str, nomer_v: str, ks: str) -> bytes:
    ensure_fonts()

    pdf = FPDF(orientation="P", unit="mm", format="A4")
    pdf.add_font("DJ",  style="",  fname=_FONT_REG)
    pdf.add_font("DJ",  style="B", fname=_FONT_BOLD)
    pdf.add_page()

    W = 210   # ширина A4, мм
    M = 20    # поля

    # Рамка
    pdf.rect(10, 10, W - 20, 277)

    # ── Логотип (пытаемся скачать при первом вызове) ──
    logo_path = os.path.join(_FONT_DIR, "doralliance_logo.png")
    logo_url  = "https://lh3.googleusercontent.com/d/1oACcpg1FQR_nrV7guMppoYOMBrSFUDqF"
    if not os.path.exists(logo_path):
        try:
            urllib.request.urlretrieve(logo_url, logo_path)
        except Exception:
            logo_path = None

    y = 22
    if logo_path and os.path.exists(logo_path):
        try:
            img_w = 35
            pdf.image(logo_path, x=(W - img_w) / 2, y=y, w=img_w)
            y += 22
        except Exception:
            pass

    # ── Название компании ──
    pdf.set_y(y)
    pdf.set_font("DJ", "B", 18)
    pdf.cell(0, 10, 'ООО «Дор-Альянс»', align="C", new_x="LMARGIN", new_y="NEXT")
    pdf.set_font("DJ", "", 11)
    pdf.set_text_color(80, 80, 80)
    pdf.cell(0, 7, "Строительство и реконструкция автомобильных дорог",
             align="C", new_x="LMARGIN", new_y="NEXT")
    pdf.set_text_color(0, 0, 0)

    # ── Горизонтальная линия ──
    y_line = pdf.get_y() + 6
    pdf.line(M + 10, y_line, W - M - 10, y_line)
    pdf.set_y(y_line + 10)

    # ── Тип документа ──
    pdf.set_font("DJ", "B", 22)
    pdf.cell(0, 12, "ИСПОЛНИТЕЛЬНАЯ", align="C", new_x="LMARGIN", new_y="NEXT")
    pdf.cell(0, 12, "ДОКУМЕНТАЦИЯ",   align="C", new_x="LMARGIN", new_y="NEXT")

    pdf.set_y(pdf.get_y() + 14)

    # ── Наименование объекта ──
    pdf.set_font("DJ", "", 10)
    pdf.set_text_color(90, 90, 90)
    pdf.cell(0, 6, "НАИМЕНОВАНИЕ ОБЪЕКТА", align="C",
             new_x="LMARGIN", new_y="NEXT")
    pdf.set_text_color(0, 0, 0)
    pdf.set_y(pdf.get_y() + 3)

    obj_text = f'«{obj_name}»' if obj_name else '«»'
    box_x = M; box_w = W - 2 * M

    # Считаем высоту поля под имя объекта
    pdf.set_font("DJ", "B", 14)
    # Минимальная высота 22 мм, увеличиваем если текст длинный
    lines = pdf.multi_cell(box_w - 6, 8, obj_text, align="C",
                           dry_run=True, output="LINES")
    box_h = max(22, len(lines) * 9 + 8)

    box_y = pdf.get_y()
    pdf.rect(box_x, box_y, box_w, box_h)
    pdf.set_xy(box_x + 3, box_y + (box_h - len(lines) * 9) / 2)
    pdf.multi_cell(box_w - 6, 9, obj_text, align="C")

    # ── Строка выполнения ──
    if nomer_v or ks:
        y_exec = box_y + box_h + 18
        pdf.line(M, y_exec, W - M, y_exec)
        pdf.set_xy(M, y_exec + 6)
        pdf.set_font("DJ", "B", 13)
        exec_text = f'Выполнение № {nomer_v or "___"}    КС-2 № {ks or "___"}'
        pdf.cell(0, 9, exec_text, align="C")

    return bytes(pdf.output())


# ─── ОБРАБОТЧИКИ ──────────────────────────────────────────────────────────────

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
    await update.message.reply_text("Панель администратора:", reply_markup=keyboard)


async def help_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text(
        "Доступные команды:\n"
        "/start — открыть программу работ\n"
        "/admin — панель администратора\n"
        "/help  — справка"
    )


async def web_app_data_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Получает данные из Mini App и возвращает PDF в чат."""
    msg = update.effective_message
    if not msg or not msg.web_app_data:
        return

    try:
        data = json.loads(msg.web_app_data.data)
    except Exception:
        return

    if data.get("type") != "pdf":
        return

    obj_name = data.get("obj", "").strip()
    nomer_v  = data.get("nomerV", "").strip()
    ks       = data.get("ks", "").strip()

    wait_msg = await msg.reply_text("⏳ Формируем PDF…")

    try:
        pdf_bytes = generate_pdf(obj_name, nomer_v, ks)
        filename  = (obj_name or "лист")[:50].strip() + ".pdf"

        await context.bot.send_document(
            chat_id=update.effective_chat.id,
            document=BytesIO(pdf_bytes),
            filename=filename,
            caption="📄 Исполнительная документация",
        )
        await wait_msg.delete()

    except Exception as e:
        logging.exception("Ошибка генерации PDF")
        await wait_msg.edit_text(f"❌ Не удалось создать PDF: {e}")


# ─── ЗАПУСК ───────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    builder = ApplicationBuilder().token(BOT_TOKEN)
    if PROXY:
        builder = builder.proxy(PROXY).get_updates_proxy(PROXY)
    app = builder.build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("admin", admin_cmd))
    app.add_handler(CommandHandler("help",  help_cmd))
    app.add_handler(MessageHandler(filters.StatusUpdate.WEB_APP_DATA, web_app_data_handler))

    print("Бот запущен. Нажмите Ctrl+C для остановки.")
    app.run_polling()
