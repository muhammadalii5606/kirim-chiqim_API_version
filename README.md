# 💰 Money Manager API

Ushbu loyiha shaxsiy moliya va hamyonlarni boshqarish uchun mo'ljallangan **REST API** tizimidir. Loyiha orqali foydalanuvchilar o'z daromad va chiqimlarini turli valyutalarda (UZS, USD va boshqalar) hisobga borishlari mumkin.

## ✨ Asosiy Imkoniyatlar
* **OTP Autentifikatsiya**: Email orqali xavfsiz va tezkor kirish.
* **Avtomatik Konvertatsiya**: Tranzaksiya valyutasi hamyon valyutasidan farq qilsa, tizim joriy kurs bo'yicha hisob-kitob qiladi.
* **Balans Nazorati**: Mablag' yetarli bo'lmaganda chiqim tranzaksiyalarini cheklash.
* **Dashboard**: Barcha hamyonlardagi pullarni yagona valyutada (UZS) ko'rish.
* **Swagger Dokumentatsiya**: API endpointlarni vizual tarzda sinab ko'rish imkoniyati.

## 🛠 Texnologiyalar
* **Backend**: Django 5.x, Django REST Framework
* **Auth**: Simple JWT (JSON Web Token)
* **Dokumentatsiya**: drf-spectacular (Swagger UI)
* **Baza**: SQLite (Loyiha kichikligi uchun tanlangan)


## 🚀 Loyihani ishga tushirish (Local)

1.  **Loyihani klon qiling:**
   

2.  **Virtual muhit yaratish va kutubxonalarni o'rnatish:**
    ```bash
    python -m venv venv
    source venv/bin/activate  # Linux/Mac uchun
    venv\Scripts\activate     # Windows uchun
    
    pip install -r requirements.txt
    ```

3.  **Bazani tayyorlash:**
    ```bash
    python manage.py migrate
    ```

4.  **Serverni yoqish:**
    ```bash
    python manage.py runserver
    ```

## 📡 API Endpoints (Qisqacha)
* `POST /api/send-otp/` - Emailga kod yuborish.
* `POST /api/verify-otp/` - Kodni tasdiqlab, token olish.
* `GET /api/dashboard/` - Umumiy balans va oxirgi amallar.
* `POST /api/transactions/create/` - Yangi tranzaksiya yaratish.
