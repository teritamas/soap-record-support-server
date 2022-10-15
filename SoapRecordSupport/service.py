import config

from SoapRecordSupport.facade.CotohaFacade import CotohaFacade
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

fb = Firebase(
    config.cred_path, 
    config.firebase_database_url,
    "feedback_comments"
)

ch = CotohaFacade(
    client_id=config.cotoha_client_id,
    client_secret=config.cotoha_client_secret
)

def _analysis_subjective_words(target_ward: str)-> list[dict]:
    """各単語の主観度を評価する

    Args:
        target_ward (str): _description_
    """
    target_words = target_ward.split("。")
    word_score = []
    for word in target_words:
        if word =="" : continue
        response = ch.predict(word)
        
        if response['result']['emotional_sentiment'] == "Neutral":
            # ニュートラルな文章であると判断された時は主観的な文章として、0.5以上のスコアを与える
            score = 0.5 - (response["result"]["score"] / 2)
        else:
            # ニュートラルな文章以外と判断された時は客観度が高い文章として、0.5以上のスコアを与える
            score = (response["result"]["score"] / 2) + 0.5
            
        word_score.append({
            "input": word,
            "score": score
        })
    return word_score

def _analysis_objective_words(target_ward: str)-> list[dict]:
    """各単語の客観度を評価する

    Args:
        target_ward (str): _description_
    """
    target_words = target_ward.split("。")
    word_score = []
    for word in target_words:
        if word =="" : continue
        response = ch.predict(word)
        
        if response['result']['emotional_sentiment'] == "Neutral":
            # ニュートラルな文章であると判断された時は客観的な文章として、0.5以上のスコアを与える
            score = (response["result"]["score"] / 2) + 0.5
        else:
            # ニュートラルな文章以外と判断された時は客観度が低いな文章として、0.5以下のスコアを与える
            score = 0.5 - (response["result"]["score"] / 2)
            
        word_score.append({
            "input": word,
            "score": score
        })
    return word_score

def evaluate(request: PostEvaluateRequestModel)-> PostEvaluateResponseModel:
    
    rec = Recommendation(
        plan="電気毛布をかける",
        assessment="これから先体温が下がりそう"
    )
    
    subjective_score: list[dict] = _analysis_subjective_words(
        request.subjective
    )
    
    objective_score: list[dict] = _analysis_objective_words(
        request.objective
    )
    
    gl = Guideline(
        category="皮膚", 
        url="https://www.dermatol.or.jp/uploads/uploads/files/guideline/Cutaneous%20angiosarcoma2021.pdf"
    )
    return PostEvaluateResponseModel(
        recommendation=rec,
        objective=[
            Objective(input=o.get('input'), score=o.get('score')) for o in objective_score
            ],
        subjective=[
            Subjective(input=o.get('input'), score=o.get('score')) for o in subjective_score
            ],
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
        "comment": content
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
        print(comment.get('name'), comment.get('comment'))
        feedback_comments.append(
            FeedBackComment(
                name=comment.get('name'), 
                feedback_comment=comment.get('comment')
            )
        )
    
    return GetFeedbackResponseModel(
        feedback_comments=feedback_comments
    )
