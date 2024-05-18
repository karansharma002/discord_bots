# Multi-Purpose Discord Bot

This bot provides various features for your Discord server:

**Features**

* **Whitelist Applications:**
    - `/application`: Guides users through a whitelist application process.
    - `/setchannel`: (Admin) Sets the channel to receive applications.
* **Twitter Rewards:**
    - `!raid <channel> <points> <tweet url>`: Creates a raid event, rewarding users for interacting with a tweet.
    - `/setchannel #channel`: (Admin) Sets the channel for reward announcements.
* **Quote System:**
    - `/quote <@user> <DD-MM-YY> <quote>`: Saves a quote from a user with the given date.
    - `/quote_random [@user]`: Retrieves a random quote from a specific user or everyone.
* **Giveaways:**
    - `/giveaway <@role> <prize>`: Starts a giveaway for the specified role.
    - `/giveaway_vc <prize>`: Starts a giveaway for members in the current voice channel.

## Setup

1. **Prerequisites:**
   - **Discord Bot:** Create a bot on the Discord Developer Portal and obtain its token.
   - **Twitter Developer Account (for Twitter rewards):** Get a Twitter developer account and create an app to obtain API keys and access tokens.
   - **Permissions:** Grant the bot the necessary permissions in the Discord server.
   - **Environment Variables:**
     - Set your Discord bot token as `TOKEN`.
     - If using Twitter rewards, set your Twitter API credentials as `TWITTER_CONSUMER_KEY`, `TWITTER_CONSUMER_SECRET`, `TWITTER_ACCESS_TOKEN`, and `TWITTER_ACCESS_SECRET`.
2. **Configuration:**
   - Create `Config.json`, `Items.json`, and `Data.json` files.
   - Use slash commands to set up channels for applications and reward announcements.

## Important Notes

* **Error Handling:** The bot includes basic error handling for missing permissions and arguments.
* **Data Storage:** The bot uses JSON files (`Config.json`, `Items.json`, `Data.json`) to store data. Make sure these files are present.
* **Dependencies:** Ensure you have installed the following libraries: `discord.py`, `tweepy`, `discord-py-slash-command`.
