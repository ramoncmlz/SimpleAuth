from fastapi import APIRouter, Depends, HTTPException, status
from datetime import datetime, timedelta

from app.schemas import (
    RegisterRequest,
    LoginRequest,
    TokenResponse,
    ChangeUsernameRequest,
    ChangePasswordRequest,
    DeleteUserRequest,
    ShowUsersRequest,
    MessageResponse,
    ShowUsersResponse
)
from app.services.user_service import (
    activate_session,
    deactivate_session,
    delete_user_by_username,
    find_user_by_username,
    list_usernames,
    register_failed_login,
    reset_login_state,
    update_password,
    update_username,
    validate_pass,
    validate_username,
    create_user,
    username_exists,
)
from app.security.jwt import create_access_token, get_current_username
from app.security.password import hash_password, verify_password

router = APIRouter()

@router.post("/register", response_model=MessageResponse)
def register(data: RegisterRequest):
    username = data.username
    password = data.password

    username_ok, error_msg = validate_username(username)

    if not username_ok:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=error_msg)
    
    if username_exists(username):
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Username already in use.",
        )

    password_ok, error_msg = validate_pass(password)
    if not password_ok:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=error_msg)

    hashed = hash_password(password)
    create_user(username, hashed)
    return MessageResponse(status="success", message=f"{username} registered successfully.")

@router.post("/login", response_model=TokenResponse | MessageResponse)
def login(data: LoginRequest):
    username = data.username
    password = data.password

    user = find_user_by_username(username)

    if user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found.")

    if int(user["session_active"]) == 1:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="This user already has an active session. Please logout first.",
        )

    if user["blocked_until"] is not None:
        blocked_until = datetime.fromisoformat(user["blocked_until"])
        if datetime.now() < blocked_until:
            remaining = blocked_until - datetime.now()
            raise HTTPException(
                status_code=status.HTTP_429_TOO_MANY_REQUESTS,
                detail=f"This user is temporarily blocked. Try again after {int(remaining.total_seconds())} seconds.",
            )
        reset_login_state(username)

    if verify_password(password, user["password"]):
        reset_login_state(username)
        session_version = activate_session(username)
        if session_version is None:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Could not start user session.",
            )

        token = create_access_token(subject=username, session_version=session_version)
        return TokenResponse(access_token=token, token_type="bearer")

    attempts_left, blocked = register_failed_login(username)
    if blocked:
        raise HTTPException(
            status_code=status.HTTP_429_TOO_MANY_REQUESTS,
            detail="You have reached 3 attempts. Try again after 3 minutes.",
        )

    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail=f"Incorrect password. Attempts left: {attempts_left}",
    )


@router.get("/me", response_model=MessageResponse)
def me(current_username: str = Depends(get_current_username)):
    return MessageResponse(status="success", message=f"Authenticated as {current_username}.")

@router.post("/logout", response_model=MessageResponse)
def logout(current_username: str = Depends(get_current_username)):
    if not deactivate_session(current_username):
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="This user is not logged in.",
        )
    return MessageResponse(status="success", message="You successfully logged out.")

@router.post("/change-username", response_model=MessageResponse)
def rename_user(data: ChangeUsernameRequest, current_username: str = Depends(get_current_username)):
    requester = data.requester
    new_username = data.new_username

    if requester != current_username:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Token user does not match requester.",
        )

    requester_user = find_user_by_username(requester)
    if requester_user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Requester not found.")

    username_ok, error_msg = validate_username(new_username)
    if not username_ok:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=error_msg)

    if username_exists(new_username):
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Username already in use.",
        )

    if not update_username(requester, new_username):
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Could not update username.",
        )

    deactivate_session(new_username)
    return MessageResponse(
        status="success",
        message=f"Username changed to {new_username}. Session closed automatically, please login again.",
    )

@router.post("/change-password", response_model=MessageResponse)
def change_pass(data: ChangePasswordRequest, current_username: str = Depends(get_current_username)):
    requester = data.requester
    new_password = data.new_password

    if requester != current_username:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Token user does not match requester.",
        )

    requester_user = find_user_by_username(requester)
    if requester_user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Requester not found.")

    password_ok, error_msg = validate_pass(new_password)
    if not password_ok:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=error_msg)

    hashed_password = hash_password(new_password)
    if not update_password(requester, hashed_password):
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Could not update password.",
        )

    return MessageResponse(
        status="success",
        message=f"User {requester} password changed successfully.",
    )

@router.delete("/delete-user", response_model=MessageResponse)
def delete_user(data: DeleteUserRequest, current_username: str = Depends(get_current_username)):
    requester = data.requester
    target = data.target

    if requester != current_username:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Token user does not match requester.",
        )

    admin_user = find_user_by_username(current_username)
    if admin_user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Requester not found.")

    if admin_user["username"] != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only admin can delete users.",
        )

    if not username_exists(target):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User to delete not found.",
        )

    if not delete_user_by_username(target):
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Could not delete user.",
        )

    return MessageResponse(status="success", message=f"User {target} deleted successfully.")

@router.get("/show-users", response_model=ShowUsersResponse | MessageResponse)
def show_users(params: ShowUsersRequest = Depends(), current_username: str = Depends(get_current_username)):
    requester = params.requester

    if requester != current_username:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Token user does not match requester.",
        )

    user = find_user_by_username(current_username)
    if user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found.")

    if user["username"] != "admin":
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Permission denied.")

    return {"users": list_usernames()}
