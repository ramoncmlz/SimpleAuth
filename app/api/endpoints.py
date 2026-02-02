from fastapi import APIRouter
from datetime import datetime, timedelta

from app.services.user_service import (
    User,
    user_list,
    get_user,
    username_exists,
    validate_username,
    validate_pass
)

router = APIRouter()

@router.post("/register")
def register(data: dict):
    username = data.get("username")
    password = data.get("password")

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

@router.post("/login")
def login(data: dict):
    username = data.get("username")
    password = data.get("password")

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

@router.post("/logout")
def logout(data: dict):
    username = data.get("username")
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

@router.post("/change-username")
def rename_user(data: dict):
    requester = data.get("requester")
    new_username = data.get("new_username")
    
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

@router.post("/change-password")
def change_pass(data: dict):
    requester = data.get("requester")
    new_password = data.get("new_password")
    
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

@router.delete("/delete-user")
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

@router.get("/show-users")
def show_users(requester: str):
    user = get_user(requester)

    if user is None:
        return {"status": "error", "message": "User not found."}

    if not user.is_logged:
        return {"status": "error", "message": "User is not logged in."}

    if user.username != "admin":
        return {"status": "error", "message": "Permission denied."}

    return [u.username for u in user_list]