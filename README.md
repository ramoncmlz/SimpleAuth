🇺🇸 English | 🇧🇷 [Português](README.pt-BR.md)

## 📌 About SimpleAuth

SimpleAuth is a **user authentication API built with FastAPI**.

The project evolved from a terminal-only login system into a real HTTP backend with persistent data, token authentication, and access control.

---

## ⚙️ Features

- User registration (`POST /register`)
- Login with JWT token (`POST /login`)
- Automatic login attempt control
- Temporary user blocking after multiple invalid attempts
- Logout with token (`POST /logout`)
- Username change with automatic session invalidation (`POST /change-username`)
- Password change (`POST /change-password`)
- Admin-only user deletion (`DELETE /delete-user`)
- Admin-only user listing (`GET /show-users`)
- Authenticated profile check (`GET /me`)

---

## 🧠 How It Works

- The API uses **SQLite** for persistence (`app/storage/simpleauth.db`).
- Passwords are stored as **hashes** (`pbkdf2_sha256` via `passlib`).
- Authentication uses **JWT Bearer tokens**.
- The system enforces one active session per user through:
  - `session_active`
  - `session_version`
- Protected endpoints read the current user from the token.

---

## 🆕 What’s New Compared To The Previous Version

- Migrated from in-memory users to **SQLite persistence**
- Replaced state flags like `is_logged` with **JWT-based auth**
- Added **hashed passwords**
- Added automatic session invalidation after username changes
- Added standardized HTTP error responses (`400`, `401`, `403`, `404`, `409`, `429`)
- Request flows were tested using Postman

---

## ▶️ How To Run

```bash
source .venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload
```

API documentation is generated automatically by Swagger.
