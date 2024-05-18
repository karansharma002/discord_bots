# Discord Google Calendar Event Reminder Bot

This Discord bot seamlessly integrates with your Google Calendar to provide timely reminders for upcoming events directly within your Discord server. It's designed to streamline communication and ensure you never miss an important event.

## Features

* **Automatic Event Reminders:**  Fetches events from your Google Calendar and sends reminders to a designated Discord channel.
* **Customizable Reminder Text:** Personalize the message that is sent for each event reminder.
* **Flexible Channel Selection:**  Choose the specific Discord channel where reminders will be posted.
* **Easy Setup:**  Simple configuration using bot commands.
* **Google Calendar Integration:** Utilizes Google's Calendar API for reliable and secure event retrieval.


## Installation

1. **Prerequisites:**
   - **Discord Bot:** Create a Discord bot and obtain its token.
   - **Google Cloud Project:** Create a Google Cloud project and enable the Google Calendar API.
   - **Service Account:** Create a service account in your project and download its JSON credentials file (`keys.json`).
   - **Bot Token:** Replace 'YOUR_TOKEN' in the script with your Discord bot's token.
2. **Setup:**
   - Place the `keys.json` file in the same directory as the script.
   - Run the script once. This will create a `Config.json` file.
   - Edit `Config.json` to set your desired channel ID and reminder text:
     ```json
     {
         "Channel": YOUR_CHANNEL_ID, 
         "Text": "YOUR_CUSTOM_REMINDER_TEXT"
     }
     ```
3. **Run the bot:** `python your_script_name.py`

## Commands

* **!setchannel \#channel:** Sets the Discord channel where event reminders will be sent.
* **!addtext [TEXT]:** Customizes the reminder message. 
* **Permissions:** The user executing these commands needs to have the `Manage Channels` permission.

## How It Works

1. The bot connects to your Google Calendar using the provided credentials.
2. Every minute, it checks for upcoming events within the next 30 minutes.
3. If a new event is found, it sends a reminder message (with your custom text) to the designated Discord channel.
4. The bot keeps track of sent events to avoid sending duplicate reminders.


## Important Notes

* **Time Zone:** The bot currently uses UTC timezone for event scheduling.
* **Permissions:** Ensure the bot has the "Send Messages" and "Embed Links" permissions in the designated channel.
* **Security:** Keep your `keys.json` file secure, as it contains sensitive credentials.


## Example Reminder

A reminder might look like this:

> **Event Alert | Team Meeting** 
> *YOUR_CUSTOM_REMINDER_TEXT*
