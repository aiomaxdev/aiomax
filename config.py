import os
from dotenv import load_dotenv

load_dotenv()

BOT_TOKEN = os.getenv("MaxToken")
WEBHOOK_URL = os.getenv("WEBHOOK_URL", None)  # Например: https://mydomain.com/webhook
WEBHOOK_SECRET = os.getenv("WEBHOOK_SECRET", "my_super_secret_key")
HOST = "0.0.0.0"
PORT = 8080
