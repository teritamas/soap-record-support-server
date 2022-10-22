from pydantic import BaseModel, Field


class PostRecordResponseModel(BaseModel):
    status: str = Field(..., title="登録が完了したかどうか")
