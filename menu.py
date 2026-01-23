from datetime import datetime, timedelta

now = datetime.now()
session_time = now.strftime("%H:%M:%S")

class User():
    def __init__(self, username, password, options):
        self.username = username
        self.password = password
        self.attempts = 3
        self.blocked_until = None
        self.options = options

# control variables
current_user = None
action = None

# not logged in menu options
guest_options = {
    1: "Login",
    2: "Register",
    3: "Exit"
}

# menu options for logged users
logged_options = {
    1: "Rename Username",
    2: "Change Password",
    3: "Logout",
    4: "Exit"
}

# menu options for admin user
admin_options = {
    1: "Delete User",
    2: "Logout",
    3: "Exit"
}

user_list = [
    User(
        username="admin",
        password="321",
        options=admin_options
    )
]

# displays the user menu and returns the choice
def show_menu(options):
    while True:
        print("Welcome to the menu.\nOptions:")
        for key, value in options.items():
            print(f"{key} - {value}")

        action = input("Select an option: ")

        if action.isdigit():
            action = int(action)
            if action in options:
                return options[action]  # returns option value
        else:
            print("Invalid option. Try again.")

# validates username rules
def validate_username(user_list, username):
    if username != username.lower():
        print("Username must be all lowercase. Try again.")
        return False

    for user in user_list:
        if user.username == username:
            print("Username already taken. Try another one.")
            return False
    return True

# validate password rules
def validate_pass(password):
    if len(password) < 8:
        print("Password must be at least 8 characters long.")
        return False
    elif password[0].islower():
        print("Password must start with an uppercase letter.")
        return False
    elif not any(c.isdigit() for c in password):
        print("Password must contain at least one number.")
        return False
    return True

# registers a new user
def register(user_list):
    while True: # username validation loop
        username = input("Create your username: ")
        if validate_username(user_list, username):
            break
    # username validated
    while True: # password validation loop
        password = input("Create a password: ")
        if validate_pass(password):
            new_user = User(
                username=username,
                password=password,
                options=logged_options
            )
            user_list.append(new_user)
            print(f"User {new_user.username} registered successfully.") # password validated
            break

# user login
def login(user_list):
    username = input("Enter your username: ")

    # searches for user in the user_list
    for user in user_list:
        if user.username == username:
            if user.blocked_until is not None: # checks if user is blocked
                if datetime.now() < user.blocked_until:
                    remaining = user.blocked_until - datetime.now()
                    print(
                        f"This user is temporarily blocked. "
                        f"Try again after {int(remaining.total_seconds())} seconds."
                    )
                    return None
                else: # unblocks the user when there is no remaining time
                    user.blocked_until = None
                    user.attempts = 3 # refresh login attempts
            # password attempts loop
            while user.attempts > 0:
                password = input("Enter your password: ")

                if password == user.password: # if its the same user password
                    print(f"You successfully logged as {username}.")
                    return user
                else:
                    user.attempts -= 1 # decreases login attempts
                    print(f"Incorrect password. Attempts left: {user.attempts}.")
            user.blocked_until = datetime.now() + timedelta(minutes=3) # blocks user for 3 minutes
            print("You have reached 3 attempts. Try again after 3 minutes.")
            return None
    # executed if user was not found in the user_list
    print("This user does not exist.")

# logs out the current user
def logout():
    print("You successfully logged out.")
    return None

# renames a user (logged only)
def rename_user(user_list, current_user):
    new_username = input("Enter your new username: ")

    for user in user_list:
        if user.username == new_username:
            print("Username already taken. Try again.")
            return

    old_username = current_user.username
    current_user.username = new_username
    print(f"User {old_username} renamed to {new_username}.")

def change_pass(current_user):
    current_password = input("Enter your current password: ")

    if current_password != current_user.password:
        print("Password does not match. Try again.")
        return

    new_password = input("Enter new password: ")
    if validate_pass(new_password):
        current_user.password = new_password
        print("Password changed successfully.")

# deletes a user (admin only)
def delete_user(user_list):
    username = input("Select user to delete: ")
    if username == "admin":
        print("User admin can not be deleted.")
        return

    for user in user_list:
        if user.username == username:
            user_list.remove(user)
            print(f"User {username} deleted.")
            return

    print("User not found.")
# show all users
def show_users(user_list):
    print("USERS:")
    for user in user_list:
        print(user.username)

print(f"Session Time: {session_time}")

while True:
    if current_user is None:
        action = show_menu(guest_options)

        if action == "Login":
            user = login(user_list)
            if user is not None:
                current_user = user

        elif action == "Register":
            register(user_list)

        elif action == "Exit":
            break

    else:
        action = show_menu(current_user.options)

        if action == "Delete User":
            show_users(user_list)
            delete_user(user_list)

        elif action == "Rename Username":
            rename_user(user_list, current_user.username)

        elif action == "Change Password":
            change_pass(current_user)

        elif action == "Logout":
            current_user = logout()

        elif action == "Exit":
            break