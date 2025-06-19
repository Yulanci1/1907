from telegram.ext import ApplicationBuilder, CommandHandler
from checker import check_slots
from telegram import Update
from telegram.ext import ContextTypes
import asyncio
import os
from dotenv import load_dotenv

load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")

async def check_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    available = await check_slots()
    msg = "🎉 Даты доступны для записи!" if available else "😔 Нет доступных дат на запись."
    await update.message.reply_text(msg)

async def notify_once(app):
    await asyncio.sleep(10)
    previous_status = None

    while True:
        try:
            current = await check_slots()
            if previous_status is None:
                previous_status = current
            elif current and not previous_status:
                await app.bot.send_message(chat_id=CHAT_ID, text="📢 Появились свободные даты на сайте VFS!")
                previous_status = current
        except Exception as e:
            await app.bot.send_message(chat_id=CHAT_ID, text=f"Ошибка при парсинге: {e}")

        await asyncio.sleep(300)

def main():
    app = ApplicationBuilder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("check", check_command))

    # Запускаем notify_once после инициализации, когда event loop уже работает
    async def post_init(app):
        asyncio.create_task(notify_once(app))

    app.post_init = post_init

    print("✅ Бот запущен")
    app.run_polling()
