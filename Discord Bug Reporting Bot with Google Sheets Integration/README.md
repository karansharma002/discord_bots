# Discord Bug Reporting Bot with Google Sheets Integration

This bot streamlines the process of bug reporting in your Discord server. It creates a dedicated channel for each report, guides users through a structured submission process, and automatically logs the reports to a Google Sheet.

## Features

* **Slash Command for Reporting:** Users initiate a bug report using the `/verify` command.
* **Dedicated Channels:** A private channel is created for each bug report, ensuring confidentiality.
* **Guided Submission:** The bot prompts users for essential details (severity, description, screenshot).
* **Google Sheets Logging:**  Reports are automatically saved to a specified Google Sheet, along with timestamps and user information.
* **Image Upload:**  Screenshots of bugs are uploaded to ImgBB for easy reference.
* **Automatic Cleanup:** The report channel is deleted after 10 seconds.

## Setup

1. **Prerequisites:**
   - **Discord Bot:** Create a bot on the Discord Developer Portal and obtain its token.
   - **Google Cloud Project:** Create a project and enable the Google Sheets API.
   - **Service Account:** Create a service account with edit access to your Google Sheet and download its JSON key file (`keys.json`).
   - **ImgBB Account:** Create an account on ImgBB and obtain an API key.
   - **Permissions:** Grant the bot the following permissions:
     - Manage Channels (to create and delete channels)
     - Send Messages
     - Read Message History
     - Attach Files
     - Embed Links
   - **Environment Variables:**
     - Set your bot token as an environment variable named `TOKEN`.
     - Set your ImgBB API key as an environment variable named `IMGBB_API_KEY`.

2. **Configuration:**
   - Replace `1061829492223529061` with the category ID where you want the bug report channels to be created.
   - Replace `1061220580671619142` with the channel ID where you want the bug report notifications to be sent.
   - Replace `1re9M1S72PzB99Nzm-1CMHG8Hn0invFOZ0gT5hQzSl5Y` with the ID of your Google Sheet.
   - Ensure that your Google Sheet has columns for timestamp, user ID, severity, description, and image link.
   - Place the `keys.json` file in the same directory as the script.

3. **Run:** Execute `python bug_report_bot.py`.

## Usage

1. **Initiating a Report:**  Type `/verify` in the desired Discord channel.
2. **Follow the Prompts:** Answer the bot's questions in the private channel created for your report.
3. **Submission:** After providing all the details, the report will be submitted to the Google Sheet and the channel will be deleted.



## Additional Notes

- **Security:** Keep your bot token and ImgBB API key confidential. Do not share these credentials publicly.
- **Customizable:** You can modify the welcome message, the questions asked by the bot, and the Google Sheet integration.
- **Error Handling:** Consider adding more comprehensive error handling for potential issues with the Google Sheets API or ImgBB.

