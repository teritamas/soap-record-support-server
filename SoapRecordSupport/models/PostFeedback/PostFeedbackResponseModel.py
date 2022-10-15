
from pydantic import BaseModel, Field


class PostFeedbackResponseModel(BaseModel):
    status: str = Field(..., title="送信が完了したかどうか")
