from SoapRecordSupport.models.LineLogin.UserInfoResponse import \
    UserInfoResponse
from SoapRecordSupport.services import fb


def set_or_get_user(group_id: str, user_id: str, name:str, code: str) -> UserInfoResponse:
    # ユーザが存在していたらそのユーザを返す
    user = fb.find_group_user(group_id, user_id)
    if not user: # 存在していなければ追加する
        user = fb.set_group_user(group_id, user_id, name, code)

    return UserInfoResponse(
        user_id=user_id,
        name=user.get('name'),
        code=code,
    )
    