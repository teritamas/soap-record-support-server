from typing import Optional

import config
import jwt
import requests
from SoapRecordSupport.models.LineLogin.LineLoginAuthenticateResponse import \
    LineLoginAuthenticateResponse
from SoapRecordSupport.models.LineLogin.LineLoginUrlResponse import \
    LineLoginLoginUrlResponse


def create_line_login_url(redirect_url: Optional[str] = None) -> LineLoginLoginUrlResponse:
    channel_id = config.line_login_channel_id
    redirect_url_ = redirect_url or config.line_login_callback_url
    random_state = "123"

    # Lineログイン用のURLの作成
    location = f"https://access.line.me/oauth2/v2.1/authorize?response_type=code&client_id={channel_id}&redirect_uri={redirect_url_}&state={random_state}&scope=openid%20profile"
    
    return LineLoginLoginUrlResponse(**{
        "message": "ok",
        "location": location,
    })

def line_get_token(code: str, redirect_url: str) -> LineLoginAuthenticateResponse:
    """ユーザ情報を取得する。

    Args:
        code (str): _description_
        redirect_url (str): _description_

    Returns:
        LineLoginAuthenticateResponse: _description_
    """
    redirect_url = redirect_url or config.line_login_callback_url
    uri_access_token = "https://api.line.me/oauth2/v2.1/token"
    headers = {"Content-Type": "application/x-www-form-urlencoded"}
    data_params = {
        "grant_type": "authorization_code",
        "code": code,
        "redirect_uri": redirect_url,
        "client_id": config.line_login_channel_id,
        "client_secret": config.line_login_channel_secret
    }

    # トークンを取得するためにリクエストを送る
    ret = requests.post(uri_access_token, headers=headers, data=data_params)

    token_response = ret.json()

    # 今回は"id_token"のみを使用する
    line_id_token = token_response["id_token"]

    # ペイロード部分をデコードすることで、ユーザ情報を取得する
    decoded_id_token = jwt.decode(line_id_token,
                                  config.line_login_channel_secret,
                                  audience=config.line_login_channel_id,
                                  issuer='https://access.line.me',
                                  algorithms=['HS256'])
    return LineLoginAuthenticateResponse(
        message= "ok",
        userId= decoded_id_token["sub"],
        name= decoded_id_token["name"],
        picture= decoded_id_token["picture"],
    )
