🇺🇸 English | 🇧🇷 [Portuguese](README.pt-BR.md)

📌 About the project

This project is a simple Python login system running in the terminal.

The idea was to simulate a basic authentication flow, with guest users, logged-in users, and an administrator user, each with different menu options.

Everything is done using only basic Python logic and structures, without a database or external libraries.

⚙️ What you can do

📝 Create new users

🔐 Log in using username and password

🚪 Log out

📋 Navigate through an interactive menu in the terminal

🛡️ Log in as admin and manage users

❌ Delete users (with protection to prevent deleting the admin)

🧠 How it works behind the scenes

Users are stored in a dictionary list containing username and password. The program controls who is logged in through the `current_user` variable.

Based on this, it decides which menu to show:

👤 No user logged in → guest menu

👥 Regular user → standard menu

🛡️ Admin → menu with extra permissions

A main loop keeps the system running until the user chooses to log out.

🎯 Project Objective

I created this project to practice programming logic in Python, mainly:

functions

lists and dictionaries

conditional structures

loops

program flow and state control

It's a simple project, but it greatly helps to understand how login systems work behind the scenes.

🚧 Next steps (under development)

🔑 Option to change the user's password, as part of the system's evolution.

🔒 Implement a security system to limit invalid login attempts

📂 Persist users in a .txt file, allowing saving and loading of registered users

🧪 Improve code validations and organization

▶️ How to run

Simply run the file in the terminal:

python user-menu.py
