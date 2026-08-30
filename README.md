# سیستم مدیریت مشاوره کنکور

سیستم کامل مدیریت مشاوره کنکور شامل ربات تلگرام و پنل مدیریت وب.

## امکانات

### ربات تلگرام (دانش‌آموز)
- ثبت‌نام و ورود به پنل شخصی
- ثبت ساعت مطالعه روزانه
- مشاهده برنامه هفتگی
- دریافت آمار و گزارش پیشرفت
- ارسال پیام به مشاور

### پنل وب (مشاور)
- داشبورد مدیریتی
- مدیریت دانش‌آموزان
- ارسال برنامه مطالعه
- مشاهده گزارش‌ها
- ارسال پیام

## نصب و راه‌اندازی

### ۱. نصب وابستگی‌ها

```bash
# API
cd api
pip install -r requirements.txt

# ربات تلگرام
cd bot
pip install -r requirements.txt

# پنل وب
cd web
npm install
```

### ۲. تنظیم متغیرهای محیطی

فایل `.env.example` را به `.env` تغییر دهید و مقادیر را پر کنید.

### ۳. اجرا

```bash
# اجرای API
cd api
uvicorn main:app --reload

# اجرای ربات تلگرام
cd bot
python main.py

# اجرای پنل وب
cd web
npm run dev
```

## استقرار روی Railway

### سرویس ۱: API
1. ریپوزیتوری را به Railway متصل کنید
2. متغیرهای محیطی را تنظیم کنید
3. فایل `railway.json` را در ریشه پروژه قرار دهید

### سرویس ۲: ربات تلگرام
1. سرویس جدیدی در Railway ایجاد کنید
2. متغیرهای محیطی را تنظیم کنید
3. فایل `railway.json` را در پوشه `bot` قرار دهید

## ساختار پروژه

```
consultant-bot/
├── api/                    # API سرور
│   ├── routes/            # مسیرهای API
│   ├── main.py           # نقطه ورودی
│   ├── database.py       # اتصال دیتابیس
│   ├── models.py         # مدل‌ها
│   └── schemas.py        # Pydantic schemas
├── bot/                    # ربات تلگرام
│   ├── handlers/         # هندلرها
│   ├── main.py           # نقطه ورودی
│   └── config.py         # تنظیمات
├── web/                    # پنل مدیریت
│   ├── app/              # صفحات Next.js
│   └── lib/              # کتابخانه‌ها
└── railway.json           # تنظیمات Railway
```

## تکنولوژی‌ها

- **Backend**: Python + FastAPI + SQLAlchemy
- **Bot**: python-telegram-bot
- **Frontend**: Next.js 14 + Tailwind CSS
- **Database**: PostgreSQL
- **Deployment**: Railway
