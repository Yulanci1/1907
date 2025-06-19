import asyncio
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
from checker import check_slots
import os
from dotenv import load_dotenv

load_dotenv()

TELEGRAM_TOKEN = os.getenv("BOT_TOKEN")
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
if previous_status is None: # Первый запуск
previous_status = current
elif current and not previous_status:
# Было False, стало True
await app.bot.send_message(chat_id=CHAT_ID, text="📢 Появились свободные даты на сайте VFS!")
previous_status = current
except Exception as e:
await app.bot.send_message(chat_id=CHAT_ID, text=f"Ошибка при парсинге: {e}")

await asyncio.sleep(300) # Каждые 5 минут
async def main():
app = ApplicationBuilder().token(BOT_TOKEN).build()

app.add_handler(CommandHandler("check", check_command))
asyncio.create_task(notify_once(app))

print("✅ Бот запущен")
await app.run_polling()
