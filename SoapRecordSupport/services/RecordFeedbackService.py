from SoapRecordSupport.models.GetFeedback.GetFeedbackResponseModel import (
    FeedBackComment, GetFeedbackResponseModel)
from SoapRecordSupport.models.PostEvaluate.PostEvaluateRequestModel import \
    PostEvaluateRequestModel
from SoapRecordSupport.models.PostEvaluate.PostEvaluateResponseModel import (
    Objective, PostEvaluateResponseModel, Recommendation, Subjective)
from SoapRecordSupport.models.PostFeedback.PostFeedbackRequestModel import \
    PostFeedbackRequestModel
from SoapRecordSupport.services import ch, fb


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
        plan="息苦しさや空咳、聴診の結果から、排痰が不十分であることが考えられる。自己排痰が困難なため、排痰を促す必要がある。",
        assessment="排痰を促すべく、吸引・体位ドレナージを行い、定期的にSpO2の観察を行う。また、場合によって呼吸リハビリテーションを実施する。"
    )
    
    subjective_score: list[dict] = _analysis_subjective_words(
        request.subjective
    )
    
    objective_score: list[dict] = _analysis_objective_words(
        request.objective
    )
    
    # S,Oに含まれるキーワードから関連するガイドラインのURLを取得する。
    keywords: list[str] = ch.keyword(target_sentence=request.objective + request.subjective)

    gl = fb.get_guideline(keywords=keywords)

    return PostEvaluateResponseModel(
        recommendation=rec,
        objective=[
            Objective(input=o.get('input'), score=o.get('score')) for o in objective_score
            ],
        subjective=[
            Subjective(input=o.get('input'), score=o.get('score')) for o in subjective_score
            ],
        guideline=gl,
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
        to_users.append(user_id)
        
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
        feedback_comments.append(
            FeedBackComment(
                name=comment.get('name'), 
                feedback_comment=comment.get('comment')
            )
        )
    
    return GetFeedbackResponseModel(
        feedback_comments=feedback_comments
    )
