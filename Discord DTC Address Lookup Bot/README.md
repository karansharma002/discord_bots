# Discord DTC Address Lookup Bot

This bot quickly looks up the DTC (Decentralized Trading Community) type associated with a given address. The data is fetched from a Google Sheet for easy maintenance.

## Features

- **Simple Command:** Use `!query <address>` to check the DTC type.
- **Google Sheets Integration:** DTC address data is stored in a Google Sheet for easy updating.
- **Error Handling:** Provides informative messages in case of errors.

## Setup

1. **Prerequisites:**
   - **Discord Bot:** Create a bot on the Discord Developer Portal and obtain its token.
   - **Google Cloud Project:** Create a project and enable the Google Sheets API.
   - **Service Account:** Create a service account in your project, grant it read access to your Google Sheet, and download its JSON key file (`keys.json`).
   - **Environment Variable:** Set your bot token as an environment variable named `TOKEN`.
2. **Configuration:**
   - Replace `SPREADSHEET_ID` and `RANGE_NAME` in the script with the ID and range of your Google Sheet.
   - Place the `keys.json` file in the same directory as the script.
3. **Run:** Execute `python query_bot.py` 

## Usage

Type `!query your_address` in a Discord channel where the bot is present. The bot will respond with an embed containing the address and its associated DTC type, if found.
