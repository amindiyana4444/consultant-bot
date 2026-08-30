from telegram import Update, ReplyKeyboardMarkup, KeyboardButton
from telegram.ext import ContextTypes
import httpx
from config import API_URL

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    keyboard = [
        [KeyboardButton("ثبت ساعت مطالعه")],
        [KeyboardButton("مشاهده برنامه"), KeyboardButton("آمار من")],
        [KeyboardButton("ارسال پیام به مشاور")]
    ]
    reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)

    async with httpx.AsyncClient() as client:
        response = await client.get(f"{API_URL}/students/")
        students = response.json()

        student_exists = any(s["telegram_id"] == user.id for s in students)

        if not student_exists:
            await update.message.reply_text(
                f"سلام {user.first_name}! 👋\n"
                "به ربات مشاور کنکور خوش آمدید.\n\n"
                "لطفاً اطلاعات خود را وارد کنید:\n"
                "نام و نام خانوادگی:"
            )
            context.user_data["registration_step"] = "name"
        else:
            await update.message.reply_text(
                f"خوش آمدید {user.first_name}! 👋\n"
                "از منوی زیر استفاده کنید:",
                reply_markup=reply_markup
            )

async def handle_registration(update: Update, context: ContextTypes.DEFAULT_TYPE):
    step = context.user_data.get("registration_step")

    if step == "name":
        context.user_data["name"] = update.message.text
        keyboard = [
            [KeyboardButton("ریاضی"), KeyboardButton("تجربی")],
            [KeyboardButton("انسانی")]
        ]
        reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
        await update.message.reply_text(
            "رشته تحصیلی خود را انتخاب کنید:",
            reply_markup=reply_markup
        )
        context.user_data["registration_step"] = "field"

    elif step == "field":
        context.user_data["field"] = update.message.text
        await update.message.reply_text(
            "سال کنکور هدف خود را وارد کنید (مثال: 1405):"
        )
        context.user_data["registration_step"] = "year"

    elif step == "year":
        try:
            year = int(update.message.text)
            user = update.effective_user

            async with httpx.AsyncClient() as client:
                await client.post(f"{API_URL}/students/", json={
                    "telegram_id": user.id,
                    "name": context.user_data["name"],
                    "field": context.user_data["field"],
                    "target_year": year
                })

            keyboard = [
                [KeyboardButton("ثبت ساعت مطالعه")],
                [KeyboardButton("مشاهده برنامه"), KeyboardButton("آمار من")],
                [KeyboardButton("ارسال پیام به مشاور")]
            ]
            reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)

            await update.message.reply_text(
                "ثبت‌نام شما با موفقیت انجام شد! ✅\n"
                "از منوی زیر استفاده کنید:",
                reply_markup=reply_markup
            )
            context.user_data.clear()

        except ValueError:
            await update.message.reply_text("لطفاً یک عدد صحیح وارد کنید:")
