
🇺🇸 English | 🇧🇷 [Português](README.pt-BR.md)

## 📌 About SimpleAuth

SimpleAuth is a **user authentication API built with FastAPI**, created to evolve a login system that previously ran only in the terminal into an **HTTP-based backend architecture**.

Using FastAPI allows separating authentication logic from the interface, making the system more organized, reusable, and ready for future integrations such as web or mobile applications.

Currently, user data is stored **in memory**, simulating real system behavior while core backend concepts are being learned.

---

## ⚙️ Current features

- 🧑‍💻 User registration via endpoint (`/register`)
- 🔐 Login with invalid attempt control
- ⏳ Temporary blocking after multiple failed attempts
- 🚪 User logout
- ✏️ Username change
- 🔄 Password change
- 🛡️ Admin user with special permissions
- ❌ User deletion (admin only)
- 📋 User listing (admin only)
- 🌐 REST API using FastAPI

---

## 🧠 How it works

- Each user is represented by a **`User` class**, containing:
  - `user_id`
  - `username`
  - `password`
  - `is_logged`
  - `attempts`
  - `blocked_until`

- Users are stored in an **in-memory list** (`user_list`).
- The API exposes endpoints that manipulate users via HTTP requests.
- Authentication state is managed using flags (`is_logged`), simulating sessions.
- The system includes:
  - username validation
  - password validation
  - login attempt control
  - temporary blocking using `datetime` and `timedelta`

---

## 🆕 What’s new compared to the previous version

- 🔁 The system no longer runs only in the terminal
- 🌐 It now works as a **REST API**
- 🧱 Uses **FastAPI** to structure routes and business logic
- 🧠 Clear separation of concerns:
  - validation
  - authentication rules
  - user management
- 🚀 Codebase prepared for real data persistence

---

## 🎯 Why FastAPI was used

FastAPI was chosen to:
- learn how authentication works in **real backend systems**
- expose features via HTTP
- prepare the project for database integration
- enable testing with tools like Postman or Swagger
- keep the code clean, scalable, and well-structured

---

## 🚧 Next steps

- 🗄️ Implement a **relational database (SQLite)** for user persistence
- 🔒 Add **password hashing** (e.g. bcrypt)
- 🧩 Replace in-memory storage with a **persistence layer**
- 🔑 Implement **token-based authentication (JWT)**
- 🧪 Improve error handling and validations

---

## ▶️ How to run

```bash
uvicorn main:app --reload

