from pydantic import BaseModel


class LineLoginLoginUrlResponse(BaseModel):
    message: str
    location: str
