from typing import Optional

from pydantic import BaseModel


class LineLoginAuthenticateResponse(BaseModel):
    message: str
    userId: str
    name: str
    picture: Optional[str] = None
