
from pydantic import BaseModel, Field


class CreateRecordResponseModel(BaseModel):
    record_id: str = Field(..., title="作成された看護記録を識別するID") 
