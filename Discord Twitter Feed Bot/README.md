# Discord Twitter Feed Bot

This bot keeps your Discord server updated with the latest tweets from a specific Twitter account. It periodically checks the Twitter feed and posts new tweets as embeds in a designated channel.

## Features

* **Automated Tweet Forwarding:** Fetches tweets from a specified Twitter user and posts them in a Discord channel.
* **Image Support:** Includes images from tweets in the embedded messages.
* **Customizable Channel:** Choose the Discord channel where the tweets will be posted.
* **Clear Command:**  Allows administrators to easily clear messages in the channel.

## Setup

1. **Prerequisites:**
   - **Discord Bot:** Create a bot on the Discord Developer Portal and obtain its token.
   - **Twitter Developer Account:** Get a Twitter developer account and create an app to get your API keys and access tokens.
   - **Permissions:**  Grant your bot the "Send Messages" and "Embed Links" permissions in the designated channel. 
   - **Environment Variables:**
     - Set your Discord bot token as `DISCORD_BOT_TOKEN`.
     - Set your Twitter API keys and tokens: `TWITTER_CONSUMER_KEY`, `TWITTER_CONSUMER_SECRET`, `TWITTER_ACCESS_TOKEN`, `TWITTER_ACCESS_SECRET`.

2. **Configuration:**
   - Open the script and replace the placeholder values (YOUR_TWITTER_CONSUMER_KEY, etc.) with your actual Twitter API credentials.
   - Run the bot once to generate the `ST.json` file.
   - Use the `!setchannel` command in your Discord server to specify the channel for tweet updates.

3. **Run the bot:** `python twitter_feed_bot.py`

## Commands

* **$setchannel #channel:** (Admin only) Sets the channel where tweets will be posted.
* **$clear [amount]:** (Admin only) Clears the specified number of messages (or 1 if not specified) from the channel.

## How It Works

1. The bot connects to the Twitter API using your provided credentials.
2. It periodically checks the specified Twitter account for new tweets (every 60 seconds by default).
3. If new tweets are found, they are formatted into Discord embeds.
4. The embeds are sent to the designated Discord channel.
5. The bot keeps track of sent tweets to avoid duplicates.

## Customization

- **Twitter User:**  Change the `screen_name` in the `api.user_timeline` call to monitor a different Twitter account.
- **Update Frequency:**  Modify the `seconds` value in the `@tasks.loop` decorator to change how often the bot checks for new tweets. 

## Important Notes

* **Rate Limits:** Be aware of Twitter's API rate limits. If you exceed them, the bot might temporarily stop working.
* **Permissions:** Make sure the bot has the necessary permissions to post embeds in the designated channel.
* **Error Handling:** Consider adding more robust error handling to the script (e.g., for network issues or invalid credentials).
