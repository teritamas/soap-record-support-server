import logging
from urllib import request

from fastapi import APIRouter

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
    return service.get_feedback()
