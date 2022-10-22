import uuid

from SoapRecordSupport.facade.Firebase import Firebase
from SoapRecordSupport.models.CreateRecord.CreateRecordResponseModel import \
    CreateRecordResponseModel
from SoapRecordSupport.models.GetRecord.GetRecordResponseModel import \
    GetRecordResponseModel
from SoapRecordSupport.models.PostRecord.PostRecordRequestModel import \
    PostRecordRequestModel
from SoapRecordSupport.models.PostRecord.PostRecordResponseModel import \
    PostRecordResponseModel
from SoapRecordSupport.services import fb


def create_record() -> CreateRecordResponseModel:
    return CreateRecordResponseModel(
        record_id=str(uuid.uuid4())
    )

def get_record(record_id: str) -> GetRecordResponseModel:
    record_dict: dict = fb.get_record(record_id=record_id)
    if record_dict:
        return GetRecordResponseModel.parse_obj(record_dict)
    else: 
        return Exception

def post_record(record_id: str, request: PostRecordRequestModel) -> PostRecordResponseModel:
    status = '';    
    try: 
        fb.set_record(record_id=record_id, content=request.dict())
        status = "ok"
    except Exception as e:
        print(e)
        status = "NG"

    return PostRecordResponseModel(
        status=status
    )
