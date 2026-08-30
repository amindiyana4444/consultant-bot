from telegram import Update
from telegram.ext import ContextTypes
import httpx
from ..config import API_URL

async def show_stats(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user

    async with httpx.AsyncClient() as client:
        response = await client.get(f"{API_URL}/students/")
        students = response.json()
        student = next((s for s in students if s["telegram_id"] == user.id), None)

        if not student:
            await update.message.reply_text("خطا: ابتدا ثبت‌نام کنید")
            return

        response = await client.get(f"{API_URL}/students/{student['id']}/stats")
        stats = response.json()

        message = (
            f"📊 آمار مطالعه شما:\n\n"
            f"کل ساعت مطالعه: {stats['total_hours']} ساعت\n"
            f"ساعت مطالعه امروز: {stats['today_hours']} ساعت\n\n"
            f"🎯 هدف: کنکور {student['target_year']}\n"
            f"📚 رشته: {student['field']}"
        )

        await update.message.reply_text(message)
