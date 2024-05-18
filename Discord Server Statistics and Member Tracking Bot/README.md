# Discord Server Statistics and Member Tracking Bot

This Discord bot provides a comprehensive view of your server's activity, including member stats, message counts, invite tracking, and more. It also sends personalized welcome messages to new members.

## Features

* **Member Statistics:** Tracks total users, online users, most active users, and total messages.
* **Channel Statistics:** Monitors the most active text channel.
* **Invite Tracking:** Logs when new members join and who invited them.  Sends a notification message to a designated channel.
* **Welcome Messages:** Sends customizable welcome messages and GIFs to new members.
* **Direct Messages:**  Can send direct messages to users through a bot command.
* **Data Persistence:** Stores data in `Data.json` for future reference.

## Setup

1. **Prerequisites:**
   - **Discord Bot:** Create a bot on the Discord Developer Portal and obtain its token.
   - **Environment Variable:** Set your bot token as an environment variable named `TOKEN`.
   - **GIF File:**  Place a GIF file (`giphy.gif`) in a `data/images` folder.
   - **Channels:** Set the appropriate channel IDs in the code for welcome messages and invite notifications.
2. **Data Storage:**
   - Create a `Data.json` file to store server statistics (start with an empty JSON object `{}`).
   - Create a `Cache.json` file to temporarily cache data (start with an empty JSON object `{}`).

## Commands

* **-send_message @user <content>:** Sends a direct message to the specified user.


## How to Use

1. **Invite the bot:** Add the bot to your server.
2. **Configuration:** Edit the channel IDs in the code.
3. **Run the bot:** `python server_stats_bot.py`
4. The bot will start tracking server activity and send welcome messages.

## Customization

- Modify the welcome message content and GIF in `on_member_join`.
- Adjust the tracking frequency in the `check_online_users` task.
