from telegram import Update
from telegram.ext import ContextTypes
import httpx
from config import API_URL, DAYS_OF_WEEK

async def show_schedule(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user

    async with httpx.AsyncClient() as client:
        response = await client.get(f"{API_URL}/students/")
        students = response.json()
        student = next((s for s in students if s["telegram_id"] == user.id), None)

        if not student:
            await update.message.reply_text("خطا: ابتدا ثبت‌نام کنید")
            return

        response = await client.get(f"{API_URL}/schedule/{student['id']}")
        schedules = response.json()

        if not schedules:
            await update.message.reply_text("برنامه‌ای برای شما ثبت نشده است.")
            return

        message = "📅 برنامه هفتگی شما:\n\n"

        for day_idx in range(7):
            day_schedules = [s for s in schedules if s["day_of_week"] == day_idx]
            if day_schedules:
                message += f"**{DAYS_OF_WEEK[day_idx]}**:\n"
                for s in day_schedules:
                    message += f"  • {s['subject']}: {s['hours']} ساعت\n"
                    if s.get("description"):
                        message += f"    ({s['description']})\n"
                message += "\n"

        await update.message.reply_text(message, parse_mode="Markdown")
