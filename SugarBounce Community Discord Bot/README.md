# SugarBounce Community Discord Bot

This bot enhances your Discord server's connection to the SugarBounce community by providing real-time notifications of live streams, tips, and UNO coin price updates. It also manages a "LIVE" role for streamers.

## Features

* **Live Stream Notifications:** Get instant updates when a SugarBounce member goes live, along with details like the streamer's name, gender, and stream link.
* **Tip Notifications:** Be alerted when tips are given between SugarBounce users.
* **UNO Price Updates:** Keep track of the current price and 24-hour price change of the UNO token.
* **LIVE Role Management:** Automatically assigns a "LIVE" role to members when they start streaming on SugarBounce.

## Setup

1. **Prerequisites:**
   - **Discord Bot:** Create a bot on the Discord Developer Portal and obtain its token.
   - **SugarBounce Account:**  Have a SugarBounce account with the necessary permissions.
   - **Environment Variables:** Create a `.env` file to store the following:
      - `DISCORD_TOKEN`: Your Discord bot token.
      - `SUGARBOUNCE_EMAIL`: Your SugarBounce email.
      - `SUGARBOUNCE_PASSWORD`: Your SugarBounce password.
      - `WEBHOOK_URL`: The webhook URL for your Discord channel.
2. **Permissions:**
   - Ensure your bot has the "Manage Roles" permission in the Discord server.
3. **Configuration:**
   - Update `DISCORD_GUILD_ID` and `DISCORD_LIVE_ROLE_ID` with your server and role IDs.
4. **Run the bot:** `python sugarbounce_bot.py` 

## How It Works

1. The bot authenticates with the SugarBounce API.
2. It periodically checks for live streams and tips on SugarBounce.
3. When a new live stream or tip is detected, the bot sends an embed notification to the configured Discord channel via webhook.
4. The bot also updates its status in Discord to display the current UNO price and 24-hour change.
5. The bot manages the "LIVE" role, assigning it to members who are streaming and removing it when they stop.


## Important Notes

* **Privacy:**  The bot only accesses public data from the SugarBounce API. It does not collect or store any private user information.
* **Rate Limits:**  The bot is set to check for updates every 5 minutes to avoid exceeding API rate limits. You can adjust the `loop` intervals if necessary.
* **Error Handling:** Basic error handling is implemented to prevent the bot from crashing if there are issues with the APIs.
