# Discord Meme & Invite Tracker Bot

This Discord bot is a multi-functional tool that keeps your community engaged. It posts random memes from Reddit to a dedicated channel and tracks member invites for your server.

## Features

* **Meme Posting:**
    - Periodically posts a random meme from the r/memes subreddit to a designated channel.
    - Customizable posting frequency (default is every 30 minutes).
* **Invite Tracking:**
    - Logs when new members join the server and who invited them.
    - Sends invite logs to a specified channel.
    - Allows members to check their own total invite count.

## Setup

1. **Prerequisites:**
   - **Discord Bot:** Create a bot on the Discord Developer Portal and obtain its token.
   - **Reddit API Credentials:**
     - Register an application on the Reddit developer portal.
     - Obtain your `client_id` and `client_secret`.
     - Set these credentials as environment variables: `REDDIT_CLIENT_ID`, `REDDIT_CLIENT_SECRET`.
   - **Permissions:** 
     - Grant the bot "Send Messages" and "Embed Links" permissions for the meme channel.
     - Grant "View Channel" for the invite logs channel.
   - **Environment Variable:** Set your bot token as an environment variable named `TOKEN`.
2. **Configuration:**
   - Use the following commands in your server:
     - `setmemechannel #channel_name`: Designate a channel for memes.
     - `setinviteschannel #channel_name`: Designate a channel for invite logs.

3. **Run the Bot:** `python meme_and_invites_bot.py` 

## Commands

* **.setinviteschannel <#channel>:** Sets the channel to send invite logs.
* **.setmemechannel <#channel>:** Sets the channel to post memes.
* **.invites:** Displays the number of invites you've sent. 

## Additional Notes

* **Customization:** You can easily change the meme source subreddit and posting frequency within the code.
* **Moderation:** Consider adding a command to delete memes if they are inappropriate.
