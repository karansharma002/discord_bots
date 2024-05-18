# Discord Google Sheets Integration Bot

This Discord bot seamlessly integrates with Google Sheets to automate the transfer of specific form responses into Discord channels and update another Google Sheet with data from your local folders. It's designed for efficiency and ease of use.

## Features

* **Form Responses to Discord:** Automatically fetches and posts new responses from a specified Google Form to a designated Discord channel.
* **Data Transfer to Google Sheets:**  Reads data from specific folders on your local machine and updates a designated Google Sheet with this information.
* **Customizable Channels:** Easily set up the Discord channels where form responses and other notifications should be sent.
* **Status Updates:** Allow authorized users (e.g., Developers, Administrators, Owners) to update the status of reported items in the Discord channel.
* **Error Handling:** Includes error logging and recovery mechanisms for a smooth operation.


## How to Use

1. **Prerequisites:**
   - **Discord Bot:** Create a Discord bot and obtain its token.
   - **Google Cloud Project:** Create a Google Cloud Project and enable the Google Sheets API.
   - **Service Account:** Create a service account in your Google Cloud Project and download its JSON key file (`keys.json`).
   - **Google Sheet:** Create a Google Sheet where you want to store the data from your local folders.

2. **Installation:**
   - Clone this repository.
   - Place the `keys.json` file in the same directory as the script.
   - Replace `SAMPLE_SPREADSHEET_ID` and `SAMPLE_RANGE_NAME` in the script with your actual Google Sheet ID and range.
   - Update `api_tokens.json` with your Discord bot token.
   - Run `pip install -r requirements.txt` to install the necessary libraries.
3. **Configuration:**
    - Use `!setchannel_1` to set the channel for form responses.
    - Use `!setchannel_2` to set the channel for data update notifications.
4. **Run the bot:** `python your_script_name.py`

## Commands

* **!status <REPORT NUMBER> <STATUS>:** Update the status of a reported item. Valid statuses are `Accepted`, `Rejected`, `Processing`, and `Fixed`.
* **!setchannel_1 <CHANNEL>`:** Set the Discord channel for form responses.
* **!setchannel_2 <CHANNEL>`:** Set the Discord channel for data update notifications.


## Configuration Files

* **`api_tokens.json`:** Store your Discord bot token here.
* **`keys.json`:**  Store your Google service account credentials here.
* **`ST1.json`, `ST2.json`:** Stores channel IDs and other settings (automatically created if not present).

## Important Notes

* Make sure your service account has read access to your Google Sheet.
* For security, keep your `keys.json` and `api_tokens.json` files private.
