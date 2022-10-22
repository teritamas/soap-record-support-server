from typing import Optional

import config
from fastapi import APIRouter, Header, HTTPException, Request
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, TextMessage, TextSendMessage

from SoapRecordSupport.models.CreateRecord.CreateRecordResponseModel import \
    CreateRecordResponseModel
from SoapRecordSupport.models.GetFeedback.GetFeedbackResponseModel import \
    GetFeedbackResponseModel
from SoapRecordSupport.models.GetRecord.GetRecordResponseModel import \
    GetRecordResponseModel
from SoapRecordSupport.models.LineLogin.LineLoginAuthenticateResponse import \
    LineLoginAuthenticateResponse
from SoapRecordSupport.models.LineLogin.LineLoginUrlResponse import \
    LineLoginLoginUrlResponse
from SoapRecordSupport.models.LineLogin.UserInfoResponse import \
    UserInfoResponse
from SoapRecordSupport.models.PostEvaluate.PostEvaluateRequestModel import \
    PostEvaluateRequestModel
from SoapRecordSupport.models.PostEvaluate.PostEvaluateResponseModel import \
    PostEvaluateResponseModel
from SoapRecordSupport.models.PostFeedback.PostFeedbackRequestModel import \
    PostFeedbackRequestModel
from SoapRecordSupport.models.PostFeedback.PostFeedbackResponseModel import \
    PostFeedbackResponseModel
from SoapRecordSupport.models.PostRecord.PostRecordRequestModel import \
    PostRecordRequestModel
from SoapRecordSupport.models.PostRecord.PostRecordResponseModel import \
    PostRecordResponseModel
from SoapRecordSupport.services import (NursingRecordService,
                                        RecordFeedbackService, handler,
                                        line_bot_api)
from SoapRecordSupport.services.Login import (create_line_login_url,
                                              line_get_token)
from SoapRecordSupport.services.Users import set_or_get_user

prefix = "/api/v1/soap-record-support"

router = APIRouter()


# 現状は看護記録を打ち分けないのでsampleに固定
RECORD_ID = "sample"
GROUP_ID = "1"

@router.get(f"{prefix}/")
def health_check():
    return {"status": "ok"}

@router.post(f"{prefix}/record", response_model=CreateRecordResponseModel)
def create_record() -> CreateRecordResponseModel:
    """新しい看護記録の作成を開始する。
    """
    return NursingRecordService.create_record()

@router.get( prefix + "/record/{record_id}", response_model=GetRecordResponseModel)
def get_record(
    record_id: str
):
    """record_idに紐づく看護記録を取得する
    """
    return NursingRecordService.get_record(record_id)

@router.post( prefix + "/record/{record_id}", response_model=PostRecordResponseModel)
def post_record(
    record_id: str,
    request: PostRecordRequestModel
):
    """看護記録を保存する
    """
    return NursingRecordService.post_record(record_id, request)

@router.post(f"{prefix}/evaluate", response_model=PostEvaluateResponseModel)
def evaluate_soap(
    request: PostEvaluateRequestModel
):
    return RecordFeedbackService.evaluate(request)

@router.post(f"{prefix}/feedback", response_model=PostFeedbackResponseModel)
def send_feedback(
    request: PostFeedbackRequestModel
):
    """他の看護師に看護記録のフィードバックを依頼する。.

    Args:
        request (PostFeedbackRequestModel): フィードバックを依頼する看護記録

    Returns:
        _type_: _description_
    """
    
    to_users: list[str] = RecordFeedbackService.get_send_users(GROUP_ID)
    converted_text: str = RecordFeedbackService.convert_line_message(request)
    
    line_bot_api.multicast(
        to=to_users,
        messages= TextSendMessage(text=converted_text),
    )
    
    return PostFeedbackResponseModel(status="ok")


@router.get(f"{prefix}/feedback", response_model=GetFeedbackResponseModel)
def get_feedback():
    """看護記録に紐づく他の看護師からのFBを返す。

    Returns:
        _type_: _description_
    """
    return RecordFeedbackService.get_feedback(RECORD_ID)


@router.post("/callback")
async def callback(request: Request, x_line_signature=Header(None)):
    """LineMessageApiのコールバック用

    Args:
        request (Request): _description_
        x_line_signature (_type_, optional): _description_. Defaults to Header(None).

    Raises:
        HTTPException: _description_

    Returns:
        _type_: _description_
    """
    body = await request.body()
    try:
        handler.handle(body.decode("utf-8"), x_line_signature)
    except InvalidSignatureError as e:
        raise HTTPException(status_code=400, detail="chatbot handle body error.")
    return 'OK'

@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    """受け取ったメッセージを、看護記録へのフィードバックとしてDBに保存する。

    Args:
        event (_type_): _description_
    """
    try:
        print(f"ユーザ情報: {event.source}")
        profile = line_bot_api.get_profile(event.source.user_id)
        RecordFeedbackService.save_feedback_message(RECORD_ID, profile.display_name, event.message.text)
        line_bot_api.reply_message(event.reply_token, TextSendMessage(text="フィードバックをくれてありがとうございます！担当者さんにお伝えしました！" ))
    except Exception as ex: 
        print(ex)


@router.get(f"{prefix}/auth/line_login", response_model=LineLoginLoginUrlResponse)
async def get_login_url(redirect_url: Optional[str] = None) -> LineLoginLoginUrlResponse:
    """Lineログイン用のURLを発行する
    """
    return create_line_login_url(redirect_url)

@router.get(f"{prefix}/auth/line_auth", response_model=UserInfoResponse)
async def authenticate(
    code: str, 
    redirect_url: Optional[str] = None
    ) -> UserInfoResponse:
    """LINEより取得した情報を、レコサポ用のユーザ情報に変換して返す。
    """
    line_info:LineLoginAuthenticateResponse = line_get_token(code, redirect_url=redirect_url)
    
    return set_or_get_user(
        group_id=GROUP_ID,
        user_id=line_info.userId,
        name=line_info.name,
        code=code
        )
