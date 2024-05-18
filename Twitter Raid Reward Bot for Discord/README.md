# Twitter Raid Reward Bot for Discord

This bot helps you incentivize and track engagement with your Twitter content. It allows you to create "raid" events on Discord where members can earn points (Gold in this case) for interacting with a specific tweet (liking, retweeting, or commenting). 

## Features

* **Raid Events:** Create raid events linked to a tweet and assign a reward value.
* **Interaction Tracking:** The bot verifies if users have liked, retweeted, or commented on the tweet.
* **Points/Rewards System:** Award points (Gold) to users for their interactions.
* **Customizable Channel:** Choose the Discord channel where raid announcements are made.

## Setup

1. **Prerequisites:**
   - **Discord Bot:** Create a bot on the Discord Developer Portal and obtain its token.
   - **Twitter Developer Account:** Get a Twitter developer account and create an app to get your API keys and access tokens.
   - **Permissions:** Grant the bot the necessary permissions in the Discord server.
   - **Environment Variables:**
     - Set your Discord bot token as `TOKEN`.
     - Set your Twitter API keys and tokens as `TWITTER_CONSUMER_KEY`, `TWITTER_CONSUMER_SECRET`, `TWITTER_ACCESS_TOKEN`, and `TWITTER_ACCESS_SECRET`.
2. **Configuration:**
   - Create `Config.json`, `Items.json`, and `Data.json` files.
   - Use the `/setchannel` command to designate a channel for raid announcements.

3. **Run the bot:** `python twitter_reward_bot.py` 

## Commands

* **!raid <channel> <points> <tweet url>:** Create a raid event. Replace placeholders with the channel, reward points, and tweet URL.
* `/setchannel #channel`: (Admin only) Set the channel for raid announcements.
* Buttons for users to claim points.

## How It Works

1. An admin uses the `!raid` command to announce a new raid event, linking to a specific tweet and specifying the reward points.
2. Users interact with the tweet on Twitter (like, retweet, comment).
3. Users click corresponding buttons on the Discord message to verify their actions.
4. The bot checks if the user has actually interacted with the tweet on Twitter.
5. If verified, the bot awards the user the specified points.


## Notes

* Ensure your Twitter API credentials are valid and have sufficient permissions to access tweets and user data.
* This bot assumes you have a points system set up in your server. 
* You can extend this bot's functionality by adding more rewards, interactions, or storing user data for leaderboards, etc.
