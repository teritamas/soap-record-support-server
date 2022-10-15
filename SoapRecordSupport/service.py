
from os import stat

from SoapRecordSupport.models.GetFeedback.GetFeedbackResponseModel import (
    FeedBackComment, GetFeedbackResponseModel)
from SoapRecordSupport.models.PostEvaluate.PostEvaluateRequestModel import \
    PostEvaluateRequestModel
from SoapRecordSupport.models.PostEvaluate.PostEvaluateResponseModel import (
    Guideline, Objective, PostEvaluateResponseModel, Recommendation,
    Subjective)
from SoapRecordSupport.models.PostFeedback.PostFeedbackResponseModel import \
    PostFeedbackResponseModel


def evaluate(request: PostEvaluateRequestModel)-> PostEvaluateResponseModel:
    
    rec = Recommendation(
        plan="電気毛布をかける",
        assessment="これから先体温が下がりそう"
    )
    sub = Subjective(
        input="寒くて震えている",
        score=0.2
    )
    ob = Objective(
        input="体温が30度",
        score=0.8
    )
    
    gl = Guideline(
        category="皮膚", 
        url="https://www.dermatol.or.jp/uploads/uploads/files/guideline/Cutaneous%20angiosarcoma2021.pdf"
    )
    return PostEvaluateResponseModel(
        recommendation=rec,
        objective=[ob],
        subjective=[sub],
        guideline=[gl],
    )


def send_line(request):
    return PostFeedbackResponseModel(status="ok")

def get_feedback():
    fb1 = FeedBackComment(
        name="田中", 
        feedback_comment="最高の看護記録です！"
    )
    fb2 = FeedBackComment(
        name="山田", 
        feedback_comment="血圧も測った方がいいですよ！"
    )
    
    return GetFeedbackResponseModel(
        feedback_comments=[fb1, fb2]
    )
