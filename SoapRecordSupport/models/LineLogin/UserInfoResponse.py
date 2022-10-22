from pydantic import BaseModel


class UserInfoResponse(BaseModel):
    user_id: str
    name: str
    code: str
