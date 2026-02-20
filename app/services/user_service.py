from datetime import datetime, timedelta

from app.storage.db import get_conn

USERNAME_ERROR_MSG = "Username must be all lowercase. Try again."
PASSWORD_MIN_LEN_ERROR_MSG = "Password must be at least 8 characters long."
PASSWORD_UPPERCASE_START_ERROR_MSG = "Password must start with an uppercase letter."
PASSWORD_NUMBER_ERROR_MSG = "Password must contain at least one number."


def ensure_username(username: str) -> str:
    if username != username.lower():
        raise ValueError(USERNAME_ERROR_MSG)
    return username


def ensure_password(password: str) -> str:
    if len(password) < 8:
        raise ValueError(PASSWORD_MIN_LEN_ERROR_MSG)
    if password[0].islower():
        raise ValueError(PASSWORD_UPPERCASE_START_ERROR_MSG)
    if not any(c.isdigit() for c in password):
        raise ValueError(PASSWORD_NUMBER_ERROR_MSG)
    return password


def validate_username(username):
    try:
        ensure_username(username)
        return True, None
    except ValueError as exc:
        return False, str(exc)


def validate_pass(password):
    try:
        ensure_password(password)
        return True, None
    except ValueError as exc:
        return False, str(exc)

def create_user(username: str, password: str):
    conn = get_conn()
    try:
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO users (username, password, session_active, attempts, blocked_until) VALUES (?, ?, ?, ?, ?)",
            (username, password, 0, 3, None)
        )
        conn.commit()
    finally:
        conn.close()

def find_user_by_username(username: str):
    conn = get_conn()
    try:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM users WHERE username = ?", (username,))
        return cursor.fetchone()
    finally:
        conn.close()

def username_exists(username: str) -> bool:
    return find_user_by_username(username) is not None


def get_session_version_by_username(username: str) -> int | None:
    user = find_user_by_username(username)
    if user is None:
        return None
    return int(user["session_version"])


def activate_session(username: str) -> int | None:
    conn = get_conn()
    try:
        cursor = conn.cursor()
        cursor.execute(
            """
            UPDATE users
            SET session_active = 1, session_version = session_version + 1
            WHERE username = ? AND session_active = 0
            """,
            (username,),
        )
        if cursor.rowcount == 0:
            conn.commit()
            return None

        cursor.execute("SELECT session_version FROM users WHERE username = ?", (username,))
        row = cursor.fetchone()
        conn.commit()
        if row is None:
            return None
        return int(row["session_version"])
    finally:
        conn.close()


def deactivate_session(username: str) -> bool:
    conn = get_conn()
    try:
        cursor = conn.cursor()
        cursor.execute(
            """
            UPDATE users
            SET session_active = 0, session_version = session_version + 1
            WHERE username = ? AND session_active = 1
            """,
            (username,),
        )
        conn.commit()
        return cursor.rowcount > 0
    finally:
        conn.close()


def reset_login_state(username: str):
    conn = get_conn()
    try:
        cursor = conn.cursor()
        cursor.execute(
            "UPDATE users SET attempts = ?, blocked_until = ? WHERE username = ?",
            (3, None, username),
        )
        conn.commit()
    finally:
        conn.close()


def register_failed_login(username: str) -> tuple[int, bool]:
    conn = get_conn()
    try:
        cursor = conn.cursor()
        cursor.execute("SELECT attempts FROM users WHERE username = ?", (username,))
        row = cursor.fetchone()
        if row is None:
            return 0, False

        attempts_left = row["attempts"] - 1
        blocked = attempts_left <= 0

        if blocked:
            blocked_until = (datetime.now() + timedelta(minutes=3)).isoformat()
            cursor.execute(
                "UPDATE users SET attempts = ?, blocked_until = ? WHERE username = ?",
                (0, blocked_until, username),
            )
            conn.commit()
            return 0, True

        cursor.execute(
            "UPDATE users SET attempts = ? WHERE username = ?",
            (attempts_left, username),
        )
        conn.commit()
        return attempts_left, False
    finally:
        conn.close()


def update_username(current_username: str, new_username: str) -> bool:
    conn = get_conn()
    try:
        cursor = conn.cursor()
        cursor.execute(
            "UPDATE users SET username = ? WHERE username = ?",
            (new_username, current_username),
        )
        conn.commit()
        return cursor.rowcount > 0
    finally:
        conn.close()


def update_password(username: str, new_password: str) -> bool:
    conn = get_conn()
    try:
        cursor = conn.cursor()
        cursor.execute(
            "UPDATE users SET password = ? WHERE username = ?",
            (new_password, username),
        )
        conn.commit()
        return cursor.rowcount > 0
    finally:
        conn.close()


def delete_user_by_username(username: str) -> bool:
    conn = get_conn()
    try:
        cursor = conn.cursor()
        cursor.execute("DELETE FROM users WHERE username = ?", (username,))
        conn.commit()
        return cursor.rowcount > 0
    finally:
        conn.close()


def list_usernames() -> list[str]:
    conn = get_conn()
    try:
        cursor = conn.cursor()
        cursor.execute("SELECT username FROM users ORDER BY username ASC")
        rows = cursor.fetchall()
        return [row["username"] for row in rows]
    finally:
        conn.close()
