from os import environ

from dotenv import load_dotenv

load_dotenv()

http_host = environ.get("HTTP_HOST", '0.0.0.0')
http_port = int(environ.get("HTTP_PORT", '8010'))

line_channel_access_token = environ.get("LINE_CHANNEL_ACCESS_TOKEN", '')
line_channel_secret = environ.get("LINE_CHANNEL_SECRET", '')

cred_path = environ.get("CRED_PATH", '')
firebase_database_url = environ.get("FIREBASE_DATABASE_URL", '')
