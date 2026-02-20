from pydantic import BaseModel


class RegisterRequest(BaseModel):
    username: str
    password: str


class LoginRequest(BaseModel):
    username: str
    password: str


class TokenResponse(BaseModel):
    access_token: str
    token_type: str


class LogoutRequest(BaseModel):
    username: str


class ChangeUsernameRequest(BaseModel):
    requester: str
    new_username: str


class ChangePasswordRequest(BaseModel):
    requester: str
    new_password: str
