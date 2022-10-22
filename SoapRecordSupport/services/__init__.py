import config
from linebot import LineBotApi, WebhookHandler
from SoapRecordSupport.facade.CotohaFacade import CotohaFacade
from SoapRecordSupport.facade.Firebase import Firebase

fire_base = Firebase(
    config.cred_path, 
    config.firebase_database_url,
    "feedback_comments"
)

cotoha_facade = CotohaFacade(
    client_id=config.cotoha_client_id,
    client_secret=config.cotoha_client_secret
)

line_bot_api = LineBotApi(config.line_channel_access_token)
handler = WebhookHandler(config.line_channel_secret)
