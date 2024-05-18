# Discord to WordPress Content Forwarding Bot

This Discord bot automatically aggregates messages from specific channels and creates daily posts on a WordPress website using the WordPress REST API. The bot is designed for users who want to archive or share Discord conversations on their websites.

## Features

- **Automated Posting:** Collects messages from specified channels and creates daily posts on WordPress.
- **Message Formatting:** Messages are formatted to preserve the author's name and timestamp.
- **Secure Authentication:** Uses Basic Authentication to connect to the WordPress REST API.

## Setup

1. **Prerequisites:**
   - **Discord Bot:** Create a bot on the Discord Developer Portal and obtain its token.
   - **WordPress Site:** Have a WordPress site with the REST API enabled.
   - **Environment Variable:** Set your bot token as an environment variable named `TOKEN`.
2. **Configuration:**
    - Create a `Config.json` file with the following structure:
      ```json
      {
        "Guilds": {
            "GUILD_ID_1": {
                "URL": "YOUR_WORDPRESS_URL",
                "Name": "YOUR_WORDPRESS_USERNAME",
                "Password": "YOUR_WORDPRESS_PASSWORD",
                "Channels": [CHANNEL_ID_1, CHANNEL_ID_2]
            }
        }
      }
      ```
    - Replace placeholders with your actual values.
    - Create a `Data.json` file to store the chat data and start with an empty JSON object `{}`.


## Usage

1. Run the bot: `python wordpress_post_bot.py`
2. Use the `!setup` command to provide your WordPress credentials. 
3. Use the `!addchannel #channel_name` command to specify which channels to monitor.
4. The bot will start collecting messages and create daily posts on your WordPress site.

## Important Notes

* Ensure your WordPress site has the REST API enabled and Basic Authentication configured.
* Keep your WordPress credentials and bot token secure.
* Consider using a dedicated user account on your WordPress site for the bot.
* Due to potential rate limits on the WordPress API, avoid adding too many channels.


