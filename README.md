## 📌 About the project

This project is a **terminal-based login system written in Python**, developed with a focus on learning programming logic, authentication, and user management.

The system allows user registration, login, and account management, with a distinction between regular users and an administrator. 
User data is stored in a **text file (`.txt`)**, simulating data persistence without using a database, including basic security validations and access attempt control.

---

- When the program starts:
  - The file is read
  - Each line is converted into a **Python dictionary**
  - Users are loaded into memory

- When the program exits:
  - Dictionaries are converted back into text
  - The file is overwritten with updated data

This process was implemented **with the help of AI**, as part of the learning process to understand **how to structure, convert, and persist data between text files and Python data structures**.

---

## 🔐 Security rules

- Username:
  - Must be lowercase only
  - Cannot be duplicated

- Password:
  - Minimum of 8 characters
  - Must start with an uppercase letter
  - Must contain at least one number

- Login:
  - 3 invalid attempts
  - 3-minute temporary block after exceeding attempts

---

## 🎯 Project goal

This project was created to **practice core backend concepts**, such as:

- authentication logic
- state control
- file manipulation
- lists and dictionaries
- validations
- basic security simulation

It is an educational project, but already structured with real-world evolution in mind.

---

## 🚧 Next steps

- 🚀 Use the **FastAPI** framework to connect the system to a database
- 🗄️ Store user data in a **SQLite** database
- 🔒 Implement **password hashing**
- 🧪 Improve validations, error handling, and code organization

---

## ▶️ How to run

```bash
python main.py

