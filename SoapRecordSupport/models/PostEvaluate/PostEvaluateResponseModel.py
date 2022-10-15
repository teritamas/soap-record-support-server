from pydantic import BaseModel, Field


class Recommendation(BaseModel):
    plan: str = Field(..., title="提案された計画")
    assessment: str = Field(..., title="提案された計画")
    
class Subjective(BaseModel):
    input: str = Field(..., title="入力で渡されたSubjectiveの内容")
    score: float = Field(..., title="その内容のスコア")

class Objective(BaseModel):
    input: str = Field(..., title="入力で渡されたObjectiveの内容")
    score: float = Field(..., title="その内容のスコア")

class Guideline(BaseModel):
    category: str = Field(..., title="入力で渡されたObjectiveの内容")
    url: str = Field(..., title="その内容のスコア")

class PostEvaluateResponseModel(BaseModel):
    recommendation: Recommendation
    subjective: list[Subjective] = []
    objective: list[Objective] = []
    guideline: list[Guideline] = []
    
