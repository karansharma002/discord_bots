# Google Forms to Discord Integration Bot

This Discord bot automatically processes responses from two Google Forms. For one form, it posts responses as embeds in a Discord channel. For the other form, it assigns a specific role to users based on their Discord ID mentioned in the responses.

## Features

* **Form Response Handling:** Fetches and processes responses from two separate Google Forms.
* **Discord Posting:** Posts responses from the first form as embeds in a designated channel.
* **Role Assignment:** Assigns a role to users based on their Discord IDs from the second form.
* **Error Handling:** Includes error handling to prevent crashes.

## Setup

1. **Prerequisites:**
   - **Discord Bot:** Create a bot on the Discord Developer Portal and obtain its token.
   - **Google Cloud Project:** Create a project and enable the Google Sheets API.
   - **Service Account:** Create a service account in your project, grant it read-only access to your Google Sheets, and download the JSON key file (`keys.json`).
   - **Environment Variable:** Set your bot's token as an environment variable named `TOKEN`.
   - **Google Forms:** Create two Google Forms and note their spreadsheet IDs.  Update the `FORM_1_SPREADSHEET_ID` and `FORM_2_SPREADSHEET_ID` variables in the script with the IDs of your Google Sheets.
2. **Configuration:**
   - Place the `keys.json` file in the same directory as the script.
   - Use the `!setchannel_1` and `!setchannel_2` commands to specify the channels for each form's responses. 
   - Make sure your bot has the "Manage Roles" permission in the server.

## Usage

1. **Run the bot:** `python google_forms_bot.py`
2. **Set Channels:** Use the commands `!setchannel_1 #channel` and `!setchannel_2 #channel` to designate channels for the responses from each form.

## Commands

* **!setchannel_1 #channel:** Sets the channel for responses from the first Google Form.
* **!setchannel_2 #channel:** Sets the channel for responses from the second Google Form.

## Additional Notes

* The bot currently fetches responses every 10 seconds for the first form and every minute for the second form. You can adjust the `loop` intervals in the `fetch_form_1` and `fetch_form_2` tasks.
* Ensure that the column headers in your Google Sheets match the expected format.
* The bot will automatically create `ST1.json` and `ST2.json` files to store settings.
* For security, keep your `keys.json` file private.
