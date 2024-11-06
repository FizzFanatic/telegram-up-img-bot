
from dotenv import load_dotenv
import os

load_dotenv()

Token = os.getenv("API_TOKEN_TELEGRAM")
url_database_telegram = os.getenv("URL_DATABASE")

WEBHOOK_URL = os.getenv("WEBHOOK_URL")

SECRET_PATH = os.getenv("SECRET_PATH")

URL_DATABASE = os.getenv("URL_DATABASE")