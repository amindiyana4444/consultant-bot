import os
from dotenv import load_dotenv

load_dotenv()

TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
API_URL = os.getenv("API_URL", "http://localhost:8000")

# For Railway: use internal URL if available
if not os.getenv("API_URL"):
    # When running in same service, use localhost
    API_URL = "http://localhost:8000"

SUBJECTS = [
    "ریاضی",
    "فیزیک",
    "شیمی",
    "زیست‌شناسی",
    "ادبیات فارسی",
    "عربی",
    "زبان انگلیسی",
    "تاریخ و جغرافیا",
    "فلسفه و منطق",
    "روانشناسی",
    "سایر"
]

DAYS_OF_WEEK = [
    "شنبه",
    "یکشنبه",
    "دوشنبه",
    "سه‌شنبه",
    "چهارشنبه",
    "پنجشنبه",
    "جمعه"
]
