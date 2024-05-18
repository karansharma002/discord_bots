import telegram
from telegram.ext import Updater, MessageHandler, Filters
from googleapiclient.discovery import build
from google.oauth2 import service_account
import datetime

# Constants
TOKEN = 'YOUR_TELEGRAM_BOT_TOKEN'  # Replace with your actual bot token
SERVICE_ACCOUNT_FILE = 'keys.json'
SCOPES = ['https://www.googleapis.com/auth/spreadsheets']
SPREADSHEET_ID = 'YOUR_SPREADSHEET_ID'
START_ROW_ID = 390

# Initialize bot and dispatcher
bot = telegram.Bot(token=TOKEN)
updater = Updater(token=TOKEN, use_context=True)
dispatcher = updater.dispatcher

row_id = START_ROW_ID

def get_google_sheets_service():
    creds = service_account.Credentials.from_service_account_file(SERVICE_ACCOUNT_FILE, scopes=SCOPES)
    return build('sheets', 'v4', credentials=creds)

def update_spreadsheet(values, row_id):
    service = get_google_sheets_service()
    sheet = service.spreadsheets()
    body = {
        'majorDimension': 'ROWS',
        'values': values
    }
    sheet.values().update(
        spreadsheetId=SPREADSHEET_ID,
        range=f"Shill Sheet!B{row_id}",
        valueInputOption="USER_ENTERED",
        body=body
    ).execute()

def fetch(update, context):
    global row_id

    text = update.message.text
    if 'twitter' in text and ('http' in text or 'https' in text):
        user = update.message.from_user.username
        sent_at = datetime.datetime.now().strftime("%d/%m/%Y")
        values = [[sent_at, user, text]]

        update_spreadsheet(values, row_id)
        row_id += 1

# Handler for all messages
echo_handler = MessageHandler(Filters.text & (~Filters.command), fetch)
dispatcher.add_handler(echo_handler)

# Start polling
updater.start_polling()
