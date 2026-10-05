# Setup and development

## Prerequisites

- Python 3.12+
- PostgreSQL available locally
- Git

## Environment

The project uses environment variables loaded from `.env`.

Example values are in `.env.example`.

## Google sign-in

Create a Google OAuth 2.0 Web application client in Google Cloud Console. Add the local callback URL `http://localhost:8000/accounts/google/login/callback/` to its authorized redirect URIs, then set `GOOGLE_OAUTH_CLIENT_ID` and `GOOGLE_OAUTH_CLIENT_SECRET` in `.env`. For deployment, add the matching HTTPS callback URL for the deployed host and configure those credentials in the deployment environment. Run `python manage.py migrate` to create the Django Sites and allauth tables.

## Database setup

The project expects a PostgreSQL database named `smart_power` for the current user. In this environment, the local Linux user `john` is used without a password, which is valid for local peer-based PostgreSQL access.

## Commands

```bash
python3 -m venv .venv
. .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
python manage.py migrate
python manage.py runserver 127.0.0.1:8000
```
