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