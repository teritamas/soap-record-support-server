from SoapRecordSupport.models.LineLogin.UserInfoResponse import \
    UserInfoResponse
from SoapRecordSupport.services import fire_base


def set_or_get_user(group_id: str, user_id: str, name:str, code: str) -> UserInfoResponse:
    # ユーザが存在していたらそのユーザを返す
    user = fire_base.find_group_user(group_id, user_id)
    if not user: # 存在していなければ追加する
        user = fire_base.set_group_user(group_id, user_id, name, code)

    return UserInfoResponse(
        user_id=user_id,
        name=user.get('name'),
        code=code,
    )
    