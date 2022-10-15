
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, TextMessage, TextSendMessage


class LineBot():
    def __init__(self, line_channel_access_token: str, line_channel_secret:str) -> None:
        self.line_bot_api = LineBotApi(line_channel_access_token)
        self.handler = WebhookHandler(line_channel_secret)


if __name__ == "__main__":
    import logging
    import os
    logging.basicConfig(level=logging.INFO)

    from dotenv import load_dotenv
    load_dotenv()
    line_channel_access_token:str = os.environ['LINE_CHANNEL_ACCESS_TOKEN']
    line_channel_secret:str= os.environ['LINE_CHANNEL_SECRET']
    
    LineBot(line_channel_access_token, line_channel_secret)
