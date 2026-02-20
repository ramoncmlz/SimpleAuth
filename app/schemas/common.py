from typing import Literal
from pydantic import BaseModel

# formatos padrão de resposta

class MessageResponse(BaseModel):
    status: Literal["success", "error"]
    message: str

