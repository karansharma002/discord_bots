# Telegram Tweet Forwarding Bot

This Telegram bot is designed to automate the collection of tweets containing links (http/https) and save them to a Google Sheet. It's a simple tool for tracking Twitter mentions, monitoring specific keywords, or gathering data for analysis.

## Features

* **Automatic Tweet Forwarding:** When a message containing "twitter" and a link is detected, the bot automatically forwards it to a Google Sheet.
* **Google Sheets Integration:** The bot seamlessly integrates with Google Sheets using a service account for authentication.
* **Data Organization:** Each forwarded tweet is saved with the timestamp and the Telegram username who sent it.

## Setup

1. **Prerequisites:**
   - **Telegram Bot:** Create a bot on BotFather and obtain its token. Replace `YOUR_TELEGRAM_BOT_TOKEN` in the script with your actual token.
   - **Google Cloud Project:** Create a Google Cloud project and enable the Google Sheets API.
   - **Service Account:** Create a service account in your project, grant it edit access to your Google Sheet, and download its JSON key file (`keys.json`).
   - **Google Sheet:** Create a Google Sheet where you want to store the tweets. Update the `SPREADSHEET_ID` in the script with your sheet's ID.

2. **Configuration:**
   - Place the `keys.json` file in the same directory as the script.
   - Update the `START_ROW_ID` variable if you want to start writing data from a specific row in the Google Sheet.

3. **Run the bot:** `python telegram_tweet_bot.py` 

## How It Works

1. The bot starts listening for messages in your Telegram chats.
2. If a message contains "twitter" and a link (http/https), it extracts the message text, username, and timestamp.
3. This data is then appended as a new row to the specified Google Sheet.

## Important Notes

* **Privacy:** This bot only forwards tweets that are publicly shared in Telegram chats where it is added. It does not access private messages or other sensitive data.
* **Permissions:** Ensure that your service account has the necessary permissions (edit access) to modify the target Google Sheet.
* **Rate Limits:** Be aware of Google Sheets API usage limits to avoid disruptions in data logging.
* **Customization:** You can easily modify the keywords or conditions to trigger tweet forwarding (e.g., specific hashtags, mentions).
