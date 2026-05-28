# HW14 Personal Essay Blog

A bilingual Korean-English personal essay blog built with Django 5.2 LTS.

## Local Setup

```powershell
cd C:\Users\user\Desktop\software_lec\hw14
.venv\Scripts\python manage.py runserver
```

Open http://127.0.0.1:8000/.

## Content Management

Create an admin account:

```powershell
.venv\Scripts\python manage.py createsuperuser
```

Then open http://127.0.0.1:8000/admin/ to manage profile, essays, categories, and tags.

Seed starter content:

```powershell
.venv\Scripts\python manage.py seed_site
```

## Styling

The active stylesheet is `static/css/site.css`, so the site works immediately without Node installed.
Tailwind config and npm scripts are included for expansion after Node LTS is installed:

```powershell
npm install
npm run build:css
```

## Deployment

Render deployment files are included:

- `requirements.txt`
- `build.sh`
- `render.yaml`

Set `ALLOWED_HOSTS` to your Render host and `CSRF_TRUSTED_ORIGINS` to `https://your-domain.onrender.com`.
