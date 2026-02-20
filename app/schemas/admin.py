from typing import List
from pydantic import BaseModel


class DeleteUserRequest(BaseModel):
    requester: str
    target: str


class ShowUsersRequest(BaseModel):
    requester: str


class ShowUsersResponse(BaseModel):
    users: List[str]
