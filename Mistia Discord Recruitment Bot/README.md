# Mistia Discord Recruitment Bot

This Discord bot streamlines the recruitment process for the Mistia server by automatically forwarding new candidate applications from Google Forms to a designated Discord channel. It also provides commands for staff members to view category-specific interview questions.

## Features

* **Automated Application Forwarding:** Fetches new applications from a specified Google Form and posts them in a Discord channel.
* **Category-Specific Questions:** Provides commands to display interview questions tailored to different roles (Graphisme, Conception, Support, Publicité).
* **Customizable:** Easily configure the Google Form ID and the Discord channel where applications are sent.
* **Error Handling:** Includes basic error handling to ensure smooth operation.

## Setup

1. **Prerequisites:**
   - **Discord Bot:** Create a Discord bot and obtain its token.
   - **Google Cloud Project:** Create a Google Cloud project and enable the Google Sheets API.
   - **Service Account:** Create a service account in your project and download its JSON key file (`keys.json`).
   - **Google Form:** Create a Google Form for applications and note its spreadsheet ID.
2. **Installation:**
   - Clone this repository.
   - Place the `keys.json` file in the same directory as the script.
   - Replace `SAMPLE_SPREADSHEET_ID` in the script with your actual Google Form's spreadsheet ID.
   - Replace `YOUR_BOT_TOKEN` with your actual bot token.
   - Run `pip install -r requirements.txt` to install the necessary libraries.
3. **Configuration:**
   - Create a `Data.json` file in the same directory as the script to track sent applications (you can start with an empty file: `{}`).

## Usage

1. **Run the bot:** `python your_script_name.py`
2. **Staff Commands:**
   - `mr.graph`: Displays interview questions for the "Graphisme" category.
   - `mr.concept`: Displays interview questions for the "Conception" category.
   - `mr.supp`: Displays interview questions for the "Support" category.
   - `mr.comm`: Displays interview questions for the "Publicité" category.

## How It Works

1. The bot periodically checks the specified Google Form for new responses.
2. When a new application is found, it formats the information into a Discord embed.
3. The embed is sent to the designated Discord channel, allowing staff to review and respond to applications.

## Customization

* You can modify the `roles` dictionary in the script to change the role IDs associated with each category.
* You can adjust the `questions` dictionary to customize the interview questions for each category.

## Important Notes

* Ensure your service account has read access to your Google Form's spreadsheet.
* Keep your `keys.json` file secure, as it contains sensitive credentials.
