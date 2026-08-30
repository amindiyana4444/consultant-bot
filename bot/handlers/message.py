from telegram import Update
from telegram.ext import ContextTypes
import httpx
from config import API_URL

async def send_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "پیام خود را برای مشاور ارسال کنید:\n"
        "(برای لغو /cancel را بزنید)"
    )
    context.user_data["waiting_message"] = True

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if context.user_data.get("waiting_message"):
        user = update.effective_user
        text = update.message.text

        if text == "/cancel":
            context.user_data.clear()
            await update.message.reply_text("پیام لغو شد.")
            return

        async with httpx.AsyncClient() as client:
            response = await client.get(f"{API_URL}/students/")
            students = response.json()
            student = next((s for s in students if s["telegram_id"] == user.id), None)

            if student:
                await client.post(f"{API_URL}/messages/", json={
                    "student_id": student["id"],
                    "sender": "student",
                    "content": text
                })
                await update.message.reply_text("✅ پیام شما ارسال شد.")
            else:
                await update.message.reply_text("خطا: ابتدا ثبت‌نام کنید")

        context.user_data.clear()
        return False
    return True
