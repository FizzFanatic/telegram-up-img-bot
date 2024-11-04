
from dotenv import load_dotenv
import os

load_dotenv()

Token = os.getenv("API_TOKEN_TELEGRAM")
url_database_telegram = os.getenv("URL_DATABASE")

