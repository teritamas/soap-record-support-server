import config

from SoapRecordSupport.facade.Firebase import Firebase
from SoapRecordSupport.models.GetFeedback.GetFeedbackResponseModel import (
    FeedBackComment, GetFeedbackResponseModel)
from SoapRecordSupport.models.PostEvaluate.PostEvaluateRequestModel import \
    PostEvaluateRequestModel
from SoapRecordSupport.models.PostEvaluate.PostEvaluateResponseModel import (
    Guideline, Objective, PostEvaluateResponseModel, Recommendation,
    Subjective)
from SoapRecordSupport.models.PostFeedback.PostFeedbackRequestModel import \
    PostFeedbackRequestModel
from SoapRecordSupport.models.PostFeedback.PostFeedbackResponseModel import \
    PostFeedbackResponseModel

fb = Firebase(
    config.cred_path, 
    config.firebase_database_url,
    "feedback_comments"
)

# def _analysis_fact_words():
    

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


def get_send_users(group_id:str)->list:
    """group_idに紐づくユーザのLineIdの一覧を取得する

    Args:
        group_id (str): _description_

    Returns:
        list: _description_
    """
    users = fb.get_group_users(group_id)
    to_users = []
    for user_id in users:
        user = users.get(user_id)
        to_users.append(user.get('line_user_id'))
        
    return to_users

def convert_line_message(request: PostFeedbackRequestModel)->str:
    return f"""看護記録のFBをお願いします！
    診療科: {request.department}
    性別: {request.sex}, 年齢: {request.age}
    --------------------
    S (主観評価): {request.subjective}
    O (客観評価): {request.objective}
    A (評価): {request.assessment}
    P (計画): {request.plan}
    """


def save_feedback_message(record_id: str, name: str, content: str):
    """フィードバックを受けたメッセージを保存する。

    Args:
        record_id (str): _description_
        name (str): _description_
        content (str): _description_
    """
    fb.add(record_id, {
        "name": name,
        "content": content
    })

def get_feedback(record_id: str):
    """看護記録に紐づくフィードバックコメントを受け取る

    Args:
        record_id (str): 検索対象のフィードバックコメント

    Returns:
        _type_: _description_
    """
    comments = fb.get_all().get(record_id)
    feedback_comments: list = []
    for comment_id in comments:
        comment = comments.get(comment_id)
        feedback_comments.append(
            FeedBackComment(
                name=comment.get('name'), 
                feedback_comment=comment.get('comment')
            )
        )
    
    return GetFeedbackResponseModel(
        feedback_comments=feedback_comments
    )
