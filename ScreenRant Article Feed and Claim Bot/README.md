# ScreenRant Article Feed and Claim Bot

This Discord bot automatically posts new articles from ScreenRant to a designated channel. Additionally, it allows members with specific roles to claim articles by reacting with a 👍 emoji, notifying administrators privately.

## Features

* **Automatic Article Posting:** Fetches and posts new articles from the ScreenRant RSS feed at regular intervals.
* **Article Claiming:**
    * Members with designated roles can claim articles by reacting with 👍.
    * Claimed articles are tracked to prevent duplicate claims.
    * Administrators receive direct messages when an article is claimed.
* **Channel Management:** Easily add or remove channels where articles are posted.
* **Role Management:** Configure which roles are allowed to claim articles.

## Installation

1. **Prerequisites:**
   - **Discord Bot:** Create a bot on the Discord Developer Portal and obtain its token. Replace `'YOUR_BOT_TOKEN'` in the script with your actual bot token.
   - **Dependencies:** Install the required libraries:
     ```bash
     pip install discord.py feedparser
     ```

2. **Configuration:**
   - Create a `Settings.json` file in the same directory as the script to store channel and role configurations (start with an empty file: `{}`).
   - Run the script once. It will create an empty `sent_titles.json` file to track posted articles.
   - Use the provided bot commands to add channels and roles as needed.

## Usage

* **Add a channel:** Use `!addchannel #channel_name` (e.g., `!addchannel #news`).
* **Remove a channel:** Use `!removechannel #channel_name`.
* **Add a role:** Use `!addrole @role_name` (e.g., `!addrole @Writers`).
* **Remove a role:** Use `!removerole @role_name`.

## How It Works

1. The bot periodically fetches the latest articles from the ScreenRant RSS feed.
2. New articles are posted to the designated channels.
3. When a user reacts with 👍 on an article post:
    - The bot checks if they have a permitted role.
    - If yes, it records the claim and notifies administrators via DM.
    - The claim is stored to prevent duplicate claims.

## Notes

* **Bot Permissions:** Ensure the bot has permission to send messages, embed links, and manage reactions in the relevant channels.
* **Rate Limits:** Be mindful of Discord's rate limits for API requests and webhooks.
* **Error Handling:** Consider adding more robust error handling for network issues or API errors.
