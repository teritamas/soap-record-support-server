from os import environ

from dotenv import load_dotenv

load_dotenv()

http_host = environ.get("HTTP_HOST", '0.0.0.0')
http_port = int(environ.get("HTTP_PORT", '8010'))
