
from pydantic import BaseModel, Field


class PostEvaluateRequestModel(BaseModel):
    department: str = Field(..., title="何科か")
    sex: str = Field(..., title="性別")
    age: int = Field(..., title="年齢")
    subjective: list[str] = Field(..., title="主観的情報")
    objective: list[str] = Field(..., title="客観的情報")
    
