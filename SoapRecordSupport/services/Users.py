from SoapRecordSupport.models.LineLogin.UserInfoResponse import \
    UserInfoResponse
from SoapRecordSupport.services import fire_base


def set_or_get_user(group_id: str, user_id: str, name:str, code: str) -> UserInfoResponse:
    user = fire_base.set_group_user(group_id, user_id, name, code)

    return UserInfoResponse(
        group_id=group_id,
        user_id=user_id,
        name=user.get('name'),
        code=code,
    )
    