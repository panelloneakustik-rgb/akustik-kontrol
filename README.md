# Akustik Kontrol

Django API (`backend/`) + Next.js vitrin (`frontend/`).

## Yerel

Python 3.13 + Node.js gerekir. Kökte `BASLAT.bat` veya:

```bat
cd backend
python -m venv venv
venv\Scripts\pip install -r requirements.txt
copy .env.example .env
venv\Scripts\python manage.py migrate
venv\Scripts\python manage.py runserver 127.0.0.1:8000
```

```bat
cd frontend
copy .env.local.example .env.local
npm install
npm run dev
```

Site: http://localhost:3000 — Admin: http://127.0.0.1:8000/admin

`.env` ve `.env.local` GitHub’a **yüklenmez**. Sunucuda sen oluşturursun (iyzico, IMAP, Google, `DJANGO_SECRET_KEY`, `DJANGO_DEBUG=false`).

## Sunucu

1. Repoyu klonla.
2. `backend/.env` ve `frontend/.env.local` doldur (`backend/.env.example` şablon).
3. `pip install -r backend/requirements.txt` + `migrate` + `collectstatic`.
4. `frontend`: `npm install` + `npm run build` + `npm start` (veya `next build` çıktısını Nginx).
5. IMAP için: `python manage.py check_invoice_emails` (cron, 5 dk).
