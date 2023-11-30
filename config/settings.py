from dotenv import load_dotenv
import os

load_dotenv()

# Environment variables are loaded here for secure access
OPENAI_KEY = os.environ.get('OPENAI_KEY')
BOT_TOKEN = os.environ.get('BOT_TOKEN')
CHANNEL_NAME = os.environ.get('CHANNEL_NAME')
SPREADSHEET_ID = os.environ.get('SPREADSHEET_ID')
CREDENTIALS_FILE = os.environ.get('CREDENTIALS_FILE')