from fastapi import FastAPI
from datetime import datetime, timedelta

app = FastAPI()


@app.get("/")
def root():
    return {"status": "ok"}

class User:
    next_id = 1
    def __init__(self, username, password):
        self.user_id = User.next_id
        User.next_id += 1
        self.username = username
        self.password = password
        self.is_logged = False
        self.attempts = 3
        self.blocked_until = None

user_list = [
    User(
        username="admin",
        password="321"
    )
]

def get_user(username):
    for user in user_list:
        if user.username == username:
            return user
    return None

def username_exists(username):
    return get_user(username) is not None

# validates username rules
def validate_username(username):
    if username != username.lower():
        error_msg = "Username must be all lowercase. Try again."
        return False, error_msg # retorna uma tupla
    return True, None
# validates password rules
def validate_pass(password):
    if len(password) < 8:
        error_msg = "Password must be at least 8 characters long."
        return False, error_msg
    elif password[0].islower():
        error_msg = "Password must start with an uppercase letter."
        return False, error_msg
    elif not any(c.isdigit() for c in password):
        error_msg = "Password must contain at least one number."
        return False, error_msg
    return True, None

@app.post("/register")
def register(username: str, password: str):
    username_ok, error_msg = validate_username(username)
    if not username_ok:
        return {"status": "error", "message": error_msg}
    if username_exists(username):
        return {"status": "error", "message": "Username already in use."}

    password_ok, error_msg = validate_pass(password)
    if not password_ok:
        return {"status": "error", "message": error_msg}

    new_user = User(username=username, password=password)
    user_list.append(new_user)

    return {
        "status": "success", "message": f"{username} registered successfully."
    }

@app.post("/login")
def login(username: str, password: str):
    user = get_user(username)

    if user is None:
        return {"status": "error", "message": "User not found."}

    if user.is_logged:
        return {
            "status": "error",
            "message": f"You already logged as {username}."
        }

    if user.blocked_until is not None:
        if datetime.now() < user.blocked_until:
            remaining = user.blocked_until - datetime.now()
            return {
                "status": "error",
                "message": f"This user is temporarily blocked. Try again after {int(remaining.total_seconds())} seconds."
            }
        else:
            user.blocked_until = None
            user.attempts = 3

    if password == user.password:
        user.is_logged = True
        user.attempts = 3
        return {
            "status": "success",
            "message": f"You successfully logged in as {username}."
        }

    # incorrect password
    user.attempts -= 1

    if user.attempts <= 0:
        user.blocked_until = datetime.now() + timedelta(minutes=3)
        return {
            "status": "error",
            "message": "You have reached 3 attempts. Try again after 3 minutes."
        }

    return {
        "status": "error",
        "message": f"Incorrect password. Attempts left: {user.attempts}"
    }

@app.post("/logout")
def logout(username: str):
    user = get_user(username)
    if user is None:
        return {"status": "error", "message": "User not found."}

    if not user.is_logged:
        return {
            "status": "error", "message": "This user is not logged in"
        }
    user.is_logged = False
    return {
        "status": "success", "message": "You successfully logged out."
    }

@app.post("/change-username")
def rename_user(requester: str, new_username: str):
    requester = get_user(requester)
    if requester is None:
        return {
            "status": "error",
            "message": "Requester not found."
        }

    if not requester.is_logged:
        return {
            "status": "error",
            "message": "Requester is not logged in."
        }

    username_ok, error_msg = validate_username(new_username)
    if not username_ok:
        return {
            "status": "error",
            "message": error_msg
        }

    if username_exists(new_username):
        return {"status": "error", "message": "Username already in use."}

    requester.username = new_username

    return {
        "status": "success",
        "message": f"Username changed to {new_username}."
    }


    #print(f"User {old_username} renamed to {new_username}.")
@app.post("/change-password")
def change_pass(requester: str, new_password: str):
    requester = get_user(requester)
    if requester is None:
        return {
            "status": "error",
            "message": "Requester not found."
        }

    if not requester.is_logged:
        return {
            "status": "error",
            "message": "Requester is not logged in."
        }

    password_ok, error_msg = validate_pass(new_password)
    if not password_ok:
        return {
            "status": "error",
            "message": error_msg
        }

    requester.password = new_password
    return {
        "status": "success", "message": f"User {requester.username} password changed successfully. ."
    }

@app.delete("/delete-user")
def delete_user(requester: str, target: str):
    admin = get_user(requester)
    if admin is None:
        return {"status": "error", "message": "Requester not found."}

    if admin.username != "admin":
        return {"status": "error", "message": "Only admin can delete users."}

    if not admin.is_logged:
        return {"status": "error", "message": "Admin is not logged in."}

    user_target = get_user(target)
    if user_target is None:
        return {"status": "error", "message": "User to delete not found."}

    user_list.remove(user_target)

    return {
        "status": "success",
        "message": f"User {target} deleted successfully."
    }

@app.get("/show-users")
def show_users(requester: str):
    user = get_user(requester)

    if user is None:
        return {"status": "error", "message": "User not found."}

    if not user.is_logged:
        return {"status": "error", "message": "User is not logged in."}

    if user.username != "admin":
        return {"status": "error", "message": "Permission denied."}

    return [u.username for u in user_list]
