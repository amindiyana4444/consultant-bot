import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from telegram import Update
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    MessageHandler,
    filters,
    ContextTypes
)
from config import TELEGRAM_TOKEN
from handlers.start import start, handle_registration
from handlers.study_log import study_log, handle_study_log
from handlers.schedule import show_schedule
from handlers.stats import show_stats
from handlers.message import send_message, handle_message

async def handle_text(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text

    if context.user_data.get("registration_step"):
        await handle_registration(update, context)
        return

    if context.user_data.get("study_step"):
        await handle_study_log(update, context)
        return

    if context.user_data.get("waiting_message"):
        await handle_message(update, context)
        return

    if text == "ثبت ساعت مطالعه":
        await study_log(update, context)
    elif text == "مشاهده برنامه":
        await show_schedule(update, context)
    elif text == "آمار من":
        await show_stats(update, context)
    elif text == "ارسال پیام به مشاور":
        await send_message(update, context)

def main():
    if not TELEGRAM_TOKEN:
        print("خطا: TELEGRAM_TOKEN تنظیم نشده است")
        return

    app = ApplicationBuilder().token(TELEGRAM_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_text))

    print("ربات شروع به کار کرد...")
    app.run_polling()

if __name__ == "__main__":
    main()
