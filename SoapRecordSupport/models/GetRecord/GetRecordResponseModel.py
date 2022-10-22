
from pydantic import BaseModel, Field


class GetRecordResponseModel(BaseModel):
    department: str = Field(..., title="何科か")
    sex: str = Field(..., title="性別")
    age: int = Field(..., title="年齢")
    subjective: str = Field(..., title="主観的情報")
    objective: str = Field(..., title="客観的情報")
    assessment: str = Field(..., title="評価コメント")
    plan: str = Field(..., title="計画")
    
