from pydantic import BaseModel, Field


class UserInfoResponse(BaseModel):
    group_id: str = Field(..., title="ユーザ属しているグループのID")
    user_id: str = Field(..., title="ユーザを一位に識別するID")
    name: str = Field(..., title="ユーザ名")
    code: str = Field(..., title="ユーザの認可コード. ログインのたびに更新される.")
