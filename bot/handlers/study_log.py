from telegram import Update, ReplyKeyboardMarkup, KeyboardButton
from telegram.ext import ContextTypes
import httpx
from config import API_URL, SUBJECTS

async def study_log(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = []
    for i in range(0, len(SUBJECTS), 2):
        row = [KeyboardButton(SUBJECTS[i])]
        if i + 1 < len(SUBJECTS):
            row.append(KeyboardButton(SUBJECTS[i + 1]))
        keyboard.append(row)
    keyboard.append([KeyboardButton("بازگشت به منو")])

    reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
    await update.message.reply_text(
        "درس مورد نظر را انتخاب کنید:",
        reply_markup=reply_markup
    )
    context.user_data["study_step"] = "subject"

async def handle_study_log(update: Update, context: ContextTypes.DEFAULT_TYPE):
    step = context.user_data.get("study_step")
    text = update.message.text

    if text == "بازگشت به منو":
        context.user_data.clear()
        keyboard = [
            [KeyboardButton("ثبت ساعت مطالعه")],
            [KeyboardButton("مشاهده برنامه"), KeyboardButton("آمار من")],
            [KeyboardButton("ارسال پیام به مشاور")]
        ]
        reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
        await update.message.reply_text("از منوی زیر استفاده کنید:", reply_markup=reply_markup)
        return

    if step == "subject":
        context.user_data["subject"] = text
        await update.message.reply_text(
            f"ساعت مطالعه {text} را وارد کنید:\n"
            "(مثال: 2.5)"
        )
        context.user_data["study_step"] = "hours"

    elif step == "hours":
        try:
            hours = float(text)
            user = update.effective_user

            async with httpx.AsyncClient() as client:
                response = await client.get(f"{API_URL}/students/")
                students = response.json()
                student = next((s for s in students if s["telegram_id"] == user.id), None)

                if student:
                    await client.post(f"{API_URL}/study/", json={
                        "student_id": student["id"],
                        "subject": context.user_data["subject"],
                        "hours": hours
                    })

                    await update.message.reply_text(
                        f"✅ ثبت شد!\n"
                        f"درس: {context.user_data['subject']}\n"
                        f"ساعت: {hours} ساعت"
                    )
                else:
                    await update.message.reply_text("خطا: ابتدا ثبت‌نام کنید")

            context.user_data.clear()
            keyboard = [
                [KeyboardButton("ثبت ساعت مطالعه")],
                [KeyboardButton("مشاهده برنامه"), KeyboardButton("آمار من")],
                [KeyboardButton("ارسال پیام به مشاور")]
            ]
            reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
            await update.message.reply_text("از منوی زیر استفاده کنید:", reply_markup=reply_markup)

        except ValueError:
            await update.message.reply_text("لطفاً یک عدد صحیح وارد کنید:")
