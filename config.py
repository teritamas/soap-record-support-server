from os import environ

from dotenv import load_dotenv

load_dotenv()

env = environ.get("ENV", 'prd')

http_host = environ.get("HTTP_HOST", '0.0.0.0')
http_port = int(environ.get("HTTP_PORT", '8010'))

line_channel_access_token = environ.get("LINE_CHANNEL_ACCESS_TOKEN", '')
line_channel_secret = environ.get("LINE_CHANNEL_SECRET", '')

line_login_channel_id = environ.get("LINE_LOGIN_CHANNEL_ID", '')
line_login_channel_secret = environ.get("LINE_LOGIN_CHANNEL_SECRET", '')
line_login_callback_url = environ.get("LINE_LOGIN_CALLBACK_URL", '')

cred_path = environ.get("CRED_PATH", '')
firebase_database_url = environ.get("FIREBASE_DATABASE_URL", '')

cotoha_client_id = environ.get("COTOHA_CLIENT_ID", '')
cotoha_client_secret = environ.get("COTOHA_CLIENT_SECRET", '')
