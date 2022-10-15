import logging
from urllib import request

import config
from fastapi import APIRouter, Header, HTTPException, Request
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, TextMessage, TextSendMessage

import SoapRecordSupport.service as service
from SoapRecordSupport.models.GetFeedback.GetFeedbackResponseModel import \
    GetFeedbackResponseModel
from SoapRecordSupport.models.PostEvaluate.PostEvaluateRequestModel import \
    PostEvaluateRequestModel
from SoapRecordSupport.models.PostEvaluate.PostEvaluateResponseModel import \
    PostEvaluateResponseModel
from SoapRecordSupport.models.PostFeedback.PostFeedbackRequestModel import \
    PostFeedbackRequestModel
from SoapRecordSupport.models.PostFeedback.PostFeedbackResponseModel import \
    PostFeedbackResponseModel

prefix = "/api/v1/soap-record-support"

router = APIRouter()

line_bot_api = LineBotApi(config.line_channel_access_token)
handler = WebhookHandler(config.line_channel_secret)

@router.get(f"{prefix}/")
def health_check():
    return {"status": "ok"}


@router.post(f"{prefix}/evaluate", response_model=PostEvaluateResponseModel)
def evaluate_soap(
    request: PostEvaluateRequestModel
):
    return service.evaluate(request)

@router.post(f"{prefix}/feedback", response_model=PostFeedbackResponseModel)
def send_feedback(
    request: PostFeedbackRequestModel
):
    return service.send_line(request)

@router.get(f"{prefix}/feedback", response_model=GetFeedbackResponseModel)
def get_feedback():
    line_bot_api.reply_message(event.reply_token, TextSendMessage(text="フィードバックをくれてありがとうございます！" ))
    
    return service.get_feedback()


@router.post("/callback")
async def callback(request: Request, x_line_signature=Header(None)):
    print("check")
    print(request)
    body = await request.body()
    try:
        handler.handle(body.decode("utf-8"), x_line_signature)
    except InvalidSignatureError as e:
        print(e)
        raise HTTPException(status_code=400, detail="chatbot handle body error.")
    return 'OK'

# MessageEvent
@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    #テキストでの返信を行う
    # line_bot_api.reply_message(
    #     event.reply_token,
    #     TextSendMessage(text=event.message.text )
    # )
    # res_data = line_bot_api.send(event.message.text)
    line_bot_api.reply_message(event.reply_token, TextSendMessage(text="フィードバックをくれてありがとうございます！" ))
