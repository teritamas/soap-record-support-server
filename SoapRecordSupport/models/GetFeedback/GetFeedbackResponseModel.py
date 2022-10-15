
from pydantic import BaseModel, Field


class FeedBackComment(BaseModel):
    name: str = Field(..., title="返答した人")
    feedback_comment: str = Field(..., title="返答内容")

class GetFeedbackResponseModel(BaseModel):
    feedback_comments: list[FeedBackComment]
    
