# Akustik Kontrol

Django API (`backend/`) + Next.js vitrin (`frontend/`).

**Canlı:** https://akustikkontrol.com.tr  
**API / admin:** https://api.akustikkontrol.com.tr/admin/

## Arkadaş / geliştirici (Windows)

1. Python 3 + Node.js LTS kur (`Add python.exe to PATH`).
2. Repoyu klonla (Collaborator daveti):  
   https://github.com/panelloneakustik-rgb/akustik-kontrol
3. Kökteki **`BASLAT.bat`** dosyasına çift tıkla.  
   `frontend` içinde `npm run dev` yazma — `next` tanınmaz.
4. Tarayıcı: http://localhost:3000 — admin: http://127.0.0.1:8000/admin  
   İlk seferde `createsuperuser` (backend venv):  
   `backend\venv\Scripts\python.exe backend\manage.py createsuperuser`

İkinci açılışta `BASLAT.bat` kurulumu atlar, sadece sunucuları açar.

## Kod → canlı

| Ne | Nasıl |
|----|--------|
| Site (Next.js) | `git push origin main` → Cloudflare Pages otomatik deploy |
| API (Django) | VM SSH: `cd ~/akustik-kontrol && git pull && sudo systemctl restart akustik` |
| Admin CSS | VM’de bir kez: `python manage.py collectstatic --noinput` |

`.env` ve `.env.local` **asla commit edilmez**. Şablon: `backend/.env.example`, `frontend/.env.local.example`. Canlı sırlar sadece VM ve Cloudflare env’de.

Yerel `.env`: `DJANGO_DEBUG=true`, `NEXT_PUBLIC_API_BASE=http://127.0.0.1:8000/api`.

## IMAP (opsiyonel)

`python manage.py check_invoice_emails` — cron / systemd timer (VM).
