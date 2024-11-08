
from dotenv import load_dotenv
import os

load_dotenv()

Token = os.getenv("API_TOKEN_TELEGRAM")
url_database_telegram = os.getenv("URL_DATABASE")

WEBHOOK_URL = os.getenv("WEBHOOK_URL")

SECRET_PATH = os.getenv("SECRET_PATH")

URL_DATABASE = os.getenv("URL_DATABASE")

ADD_CREDIT_TO_START = 10 # одноразовый бонус за вступление

PUBLIC_KEY_I_LOVE_API = os.getenv("PUBLIC_KEY_I_LOVE_API")

PRIVATE_KEY_I_LOVE_API = os.getenv("PRIVATE_KEY_I_LOVE_API")